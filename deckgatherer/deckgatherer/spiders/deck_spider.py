from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from deckgatherer.items import DeckItem
from bs4 import BeautifulSoup
import requests


class DeckSpider(CrawlSpider):
    name = "deck_spider"
    start_urls = [
        "http://www.mtgdecks.net/events/viewByFormat/39/"
    ]

    rules = [
        Rule(LinkExtractor(allow=(r"decks/view/\d+$", )), callback="parse_item"),
        Rule(LinkExtractor(allow=(r"events/view/\d+$", ))),
        Rule(LinkExtractor(allow=(r"events/viewByFormat/39/page:\d+$", ))),
    ]

    def parse_item(self, response):
        self.log("item page: %s" % response.url)
        deck = DeckItem()
        soup = BeautifulSoup(response.body)

        try:
            deck["name"] = soup.find_all(
                "div",
                class_="deckInfo col-md-8"
            )[0].find_all("strong")[0].contents[0].string.split(".")[0]

        except IndexError:
            print "Deck name not found"
            deck["name"] = ""

        try:
            deck["rank"] = soup.find_all(
                "div",
                class_="col-md-12 sidebar"
            )[0].find_all('li')[1].contents[1].string.strip()

            if deck["rank"].lower() == "other":
                return

        except IndexError:
            print "Deck rank not found"
            deck["rank"] = "0"

        try:
            deck["event_name"] = soup.find_all(
                "div",
                class_="col-md-12 sidebar"
            )[0].find_all('li')[0].contents[1].string.strip()

            deck["event_participants"] = soup.find_all(
                "div",
                class_="col-md-12 sidebar"
            )[0].find_all('li')[2].contents[1].string.strip()

            if not deck["event_participants"].isdigit():
                deck["event_participants"] = "36"  # assumption, but standard event size

            deck["event_date"] = soup.find_all(
                "div",
                class_="col-md-12 sidebar"
            )[0].find_all('li')[4].contents[1].string.strip()

        except IndexError:
            print "Deck event information not found"

        try:
            raw_deck_url = soup.find_all(
                "div",
                class_="btn-group"
            )[0].find_all("a")[1]["href"]

            req = requests.get("http://mtgdecks.net" + raw_deck_url)
            if req.text is None:
                return

            deck["raw_deck"] = req.text

        except Exception:
            print "Raw deck could not be retrieved"
            deck["raw_deck"] = None

        return deck
