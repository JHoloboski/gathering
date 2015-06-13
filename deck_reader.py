"""
Reads in a simple mtgo deck file, which is just a txt file delimited by
newlines
"""
from deck import Deck


class DeckReader(object):
    def __init__(self, deck_file):
        self.deck_file = deck_file

    def __repr__(self):
        return "{0}, {1}".format(
            self.__class__.__name__,
            self.deck_file
        )

    def make_deck(self):
        """
        Extracts the information from the deck file into a deck dictionary
        with two primary elements, "main" which is for the main deck, and
        "side" for the sideboard. We're keeping track of each individual
        card name and count.
        """
        with open(self.deck_file, 'r') as deck_file:
            in_sideboard = False
            deck = {}
            deck["main"] = {}
            deck["side"] = {}

            for cards in deck_file:
                if cards.lower().strip() == "sideboard":
                    in_sideboard = True
                    continue

                count, card_name = cards.split(" ", 1)
                card_name = card_name.strip()

                if in_sideboard:
                    deck["side"][card_name] = count
                else:
                    deck["main"][card_name] = count

        return Deck(deck["main"], deck["side"])
