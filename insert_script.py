import sys
import ast

from deckanalyzer.deck_reader import DeckReader


def main(deck_file):
    """
    Reads in the individual deck records that were scraped, puts them in the db
    """
    reader = DeckReader()
    with open(deck_file, 'r') as decks:
        for deck in decks:
            deck = ast.literal_eval(deck)  # these decks are dicts
            reader.read_deck(deck)


if __name__ == "__main__":
    main(sys.argv[1])  # just a simple script, just takes 1 argument
