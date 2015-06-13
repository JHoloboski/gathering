"""
Simple deck object
May later be replaced with a model to be used with a db
"""
import requests


class Deck(object):
    def __init__(self, main, side):
        # Will eventually need more data here including rank,
        # date, total count in main/side, maybe defining colors, CMC for sure
        # might just end up becoming a sqlalchemy model honestly
        self.main_deck = main
        self.sideboard = side
        self.detailed_main = {}
        self.detailed_side = {}

        self._get_card_info()

    def __repr__(self):
        return "Main deck: {0}, Sideboard: {1}".format(
            self.main,
            self.side
        )

    def _get_card_info(self):
        """
        Test using the mtgapi, probably will be removed
        """
        for key in self.main_deck.keys():
            data = {"name": key}
            req = requests.get("http://api.mtgapi.com/v2/cards", params=data)
            self.detailed_main[key] = req.json()
            self.detailed_main[key]["count"] = self.main_deck[key]

        for key in self.sideboard.keys():
            data = {"name": key}
            req = requests.get("http://api.mtgapi.com/v2/cards", params=data)
            self.detailed_side[key] = req.json()
            self.detailed_side[key]["count"] = self.sideboard[key]
