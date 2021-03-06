# -*- coding: utf8 -*-
"""
Reads in a simple mtgo deck file, which is just a txt file delimited by
newlines
"""
import requests
import deckanalyzer.models as models
from deckanalyzer.models import card, cards_in_decks, deck, event

import re
import sys
from collections import namedtuple
from sqlalchemy.sql import func


FullDeck = namedtuple("FullDeck", ["main_deck", "sideboard"])


class DeckReader(object):
    """
    Reads in an individual deck and performs all necessary additions
    and updates for the deck into the database
    """
    def add_deck(self, deck_info):
        """
        Add deck to the database
        """
        rank = int(re.sub("\D", "", deck_info["rank"]))

        event_id = self.get_or_add_event(
            deck_info["event_name"],
            deck_info["event_date"],
            deck_info["event_participants"]
        )

        new_deck = deck.Deck(
            name=deck_info["name"],
            event_id=event_id,
            rank=rank
        )

        with models.session() as session:
            session.add(new_deck)
            session.flush()

            return new_deck.id

    def add_deck_contents(self, deck_info):
        """
        Read in the deck's information and create the card, deck, and
        relationship records in the database
        """
        full_deck = self._create_deck(deck_info["raw_deck"])
        deck_id = self.add_deck(deck_info)

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
                    deck_id=deck_id,
                    card_id=card_id,
                    main_quantity=main_count,
                    side_quantity=side_count
                )
                session.add(new_cid)

            for mtg_card in full_deck.sideboard.keys():
                main_count = 0
                side_count = full_deck.sideboard[mtg_card]

                card_id = self.get_or_add_card(mtg_card)

                new_cid = cards_in_decks.CardsInDecks(
                    deck_id=deck_id,
                    card_id=card_id,
                    main_quantity=main_count,
                    side_quantity=side_count
                )
                session.add(new_cid)

        return deck_id

    def calculate_avg_cmc(self, deck_id):
        """
        Calculate the average converted mana cost of a deck.
        """
        with models.session() as session:
            avg_cmc = session.query(
                (
                    func.sum(card.Card.cmc * cards_in_decks.CardsInDecks.main_quantity) /
                    func.sum(cards_in_decks.CardsInDecks.main_quantity)
                )
            ).join(
                card.Card,
                card.Card.id == cards_in_decks.CardsInDecks.card_id
            ).filter(
                cards_in_decks.CardsInDecks.deck_id == deck_id,
                cards_in_decks.CardsInDecks.main_quantity > 0,
                card.Card.is_land == 0
            ).scalar()

            return avg_cmc

    def calculate_lands(self, deck_id, is_land):
        """
        Count the number of land cards in a deck
        """
        with models.session() as session:
            card_count = session.query(
                func.sum(cards_in_decks.CardsInDecks.main_quantity)
            ).join(
                card.Card,
                card.Card.id == cards_in_decks.CardsInDecks.card_id
            ).filter(
                cards_in_decks.CardsInDecks.deck_id == deck_id,
                card.Card.is_land == is_land
            ).scalar()

            return card_count

    def calculate_weighted_rank_value(self, deck_id):
        """
        Determine the weighted rank value based on how the deck ranked in
        relation to the number of players involved in the event the deck was
        used in
        """
        with models.session() as session:
            weighted_rank_value = session.query(
                event.Event.number_of_players / deck.Deck.rank
            ).join(
                event.Event,
                event.Event.id == deck.Deck.event_id
            ).filter(
                deck.Deck.id == deck_id
            ).scalar()

            return weighted_rank_value

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
            try:
                card_info = card_info["cards"][0]
            except TypeError:
                print "TypeError caught, card info was: {0}".format(card_info)
                sys.exit(-1)

            new_card = card.Card(
                name=card_name,
                mana_cost=card_info["manaCost"],
                cmc=int(card_info["cmc"]),
                text=card_info["text"],
                power=card_info["power"],
                toughness=card_info["toughness"]
            )

            self._set_card_types(new_card, card_info["types"])

            session.add(new_card)
            session.flush()

            return new_card.id

    def get_or_add_event(self, name, date, participants):
        """
        Add an event to the database, if it's not already there
        """
        with models.session as session:
            dupe_event = session.query(
                event.Event.id
            ).filter(
                event.Event.name == name,
                event.Event.event_date == date
            )

            if dupe_event is not None:
                return dupe_event.id

            new_event = event.Event(
                name=name,
                event_date=date,
                format_id=1,  # Will eventually need to be pulled from db
                number_of_players=participants
            )

            session.add(new_event)
            session.flush()

            return new_event.id

    def perform_calculations(self, deck_id):
        """
        Perform calculations on the deck's contents and then update the deck
        """
        weighted_rank_value = self.calculate_weighted_rank_value(deck_id)
        avg_cmc = self.calculate_avg_cmc(deck_id)
        lands = self.calculate_lands(deck_id, True)
        non_lands = self.calculate_lands(deck_id, False)

        with models.session() as session:
            session.query(deck.Deck).filter(
                deck.Deck.id == deck_id
            ).update({
                deck.Deck.weighted_rank_value: weighted_rank_value,
                deck.Deck.avg_cmc: avg_cmc,
                deck.Deck.lands: lands,
                deck.Deck.non_lands: non_lands
            })

            session.commit()

    def read_deck(self, deck_info):
        """
        Main method to have deck reader perform all methods on information
        passed in
        """
        deck_id = self.add_deck_contents(deck_info)
        self.perform_calculations(deck_id)

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
            if line == "":
                continue

            count, card_name = line.split(" ", 1)
            if "Aether" in card_name:
                card_name = card_name.replace("Aether", "Æther")
            if in_sideboard:
                full_deck.sideboard[card_name] = int(count)
            else:
                full_deck.main_deck[card_name] = int(count)

        return full_deck

    @staticmethod
    def _set_card_types(new_card, types):
        """
        Set types on the card based on the list mtgapi returns for it
        """
        types = [t.lower() for t in types]

        if "artifact" in types:
            new_card.is_artifact = True
        if "creature" in types:
            new_card.is_creature = True
        if "enchantment" in types:
            new_card.is_enchantment = True
        if "instant" in types:
            new_card.is_instant = True
        if "land" in types:
            new_card.is_land = True
        if "planeswalker" in types:
            new_card.is_planeswalker = True
        if "sorcery" in types:
            new_card.is_sorcery = True
