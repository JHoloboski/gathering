"""
Reads in a simple mtgo deck file, which is just a txt file delimited by
newlines
"""
import requests
import deckanalyzer.models as models
from deckanalyzer.models import card


class DeckReader(object):
    def __init__(self, deck):
        self.deck = deck

    def __repr__(self):
        return "{0}, {1}".format(
            self.__class__.__name__,
            self.deck
        )

    @staticmethod
    def get_or_add_card(card_name):
        """
        Add card to the database if it's not already there
        """
        with models.session() as session:
            cards = session.query(
                card.Card.id
            ).filter(
                card.Card.name == card_name
            ).first()

            if cards.count() > 0:
                return

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
