"""
Reads in a simple mtgo deck file, which is just a txt file delimited by
newlines
"""
import requests
import deckanalyzer.models as models
from deckanalyzer.models import card, cards_in_decks, deck

import re
from collections import namedtuple
from sqlalchemy.sql import func


FullDeck = namedtuple("FullDeck", ["main_deck", "sideboard"])


class DeckReader(object):
    def __init__(self, deck_info):
        self.deck_info = deck_info  # an individual deck from the spider

    def __repr__(self):
        return "{0}, {1}".format(
            self.__class__.__name__,
            self.deck
        )

    def add_deck(self):
        """
        Add deck to the database
        """
        rank = int(re.sub("\D", "", self.deck_info["rank"]))

        new_deck = deck.Deck(
            name=self.deck_info["name"],
            format_id=1,  # will eventually need to be grabbed from db
            rank=rank
        )

        with models.session() as session:
            session.add(new_deck)
            session.flush()

            return new_deck.id

    def add_deck_contents(self):
        """
        Read in the deck's information and create the card, deck, and
        relationship records in the database
        """
        full_deck = self._create_deck(self.deck_info["raw_deck"])
        deck_id = self.add_deck()

        with models.session() as session:
            # Adding the cards from the main deck
            for mtg_card in full_deck.main_deck.keys():
                main_count = full_deck.main_deck[mtg_card]
                side_count = 0

                if mtg_card in full_deck.sideboard:
                    side_count = full_deck.sideboard[mtg_card]
                    full_deck.sideboard.pop(mtg_card)

                card_id = self.get_or_add_card(mtg_card)

                new_cid = cards_in_decks.CardsInDecks(
                    deck_id,
                    card_id,
                    main_count,
                    side_count
                )
                session.add(new_cid)

            for mtg_card in full_deck.sideboard.keys():
                main_count = 0
                side_count = full_deck.sideboard[mtg_card]

                card_id = self.get_or_add_card(mtg_card)

                new_cid = cards_in_decks.CardsInDecks(
                    deck_id,
                    card_id,
                    main_count,
                    side_count
                )
                session.add(new_cid)

    def calculate_avg_cmc(self, deck_id):
        """
        Calculate the average converted mana cost of a deck.
        """
        with models.session() as session:
            query = session.query(
                func.avg(card.Card.cmc)
            ).join(
                cards_in_decks.CardsInDecks,
                card.Card.id == cards_in_decks.CardsInDecks.card_id
            ).filter(
                cards_in_decks.CardsInDecks.deck_id == deck_id
            )

            avg_cmc = query.one()[0]

            # TODO: Move the update for all calculated metrics into one place
            session.query(deck.Deck).filter(
                deck.Deck.id == deck_id
            ).update({
                deck.Deck.avg_cmc: avg_cmc
            })

            session.commit()

    def get_or_add_card(self, card_name):
        """
        Add card to the database if it's not already there
        """
        with models.session() as session:
            dupe_card = session.query(
                card.Card.id
            ).filter(
                card.Card.name == card_name
            ).first()

            if dupe_card is not None:
                return dupe_card.id

            data = {"name": card_name}
            req = requests.get("http://api.mtgapi.com/v2/cards", params=data)
            card_info = req.json()
            card_info = card_info["cards"][0]

            new_card = card.Card(
                name=card_name,
                mana_cost=card_info["manaCost"],
                cmc=int(card_info["cmc"]),
                types=card_info["types"],
                text=card_info["text"],
                power=int(card_info["power"]),
                toughness=int(card_info["toughness"])
            )

            session.add(new_card)
            session.flush()

            return new_card.id

    @staticmethod
    def _create_deck(deck_contents):
        """
        Split the raw contents of a deck into the main and sideboard
        """
        deck_contents = deck_contents.split("\n")
        full_deck = FullDeck({}, {})

        in_sideboard = False
        for line in deck_contents:
            if line.lower().strip() == "sideboard":
                in_sideboard = True
                continue

            count, card_name = line.split(" ", 1)
            if in_sideboard:
                full_deck.sideboard[card_name] = int(count)
            else:
                full_deck.main_deck[card_name] = int(count)

        return full_deck
