class DeckReader(object):
    def __init__(self, deck_file):
        self.deck_file = deck_file

    def make_deck(self):
        try:
            deck = open(self.deck_file, 'r')
            in_sideboard = False
            self.main_deck = {}
            self.sideboard = {}

            for cards in deck:
                if cards.lower().strip() == "sideboard":
                    in_sideboard = True
                    continue

                count, card_name = cards.split(" ", 1)
                card_name = card_name.strip()

                if in_sideboard:
                    self.sideboard[card_name] = count
                else:
                    self.main_deck[card_name] = count

        except IOError:
            print "File {0} not found".format(self.deck_file)

        finally:
            deck.close()
