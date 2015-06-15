import re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from deckretriever.items import DeckItem
from bs4 import BeautifulSoup


class DeckSpider(CrawlSpider):
    name = 'deck_spider'
    start_urls = [
        'www.mtgdecks.net/events/viewByFormat/37/'
    ]

    rules = [
        Rule(LinkExtractor(allow=(r'decks/view/\d+', )), callback='parse_item'),
        Rule(LinkExtractor(allow=(r'events/view/\d+', ))),
        Rule(LinkExtractor(allow=(r'events/viewByFormat/37/page:\d+', ))),
    ]

    def parse_item(self, response):
        self.log('item page: %s' % response.url)
        deck = DeckItem()
        soup = BeautifulSoup(response.body)

        rank_list = soup.find_all(
            'div',
            class_='col-md-12 sidebar'
        )[0].find_all('li')[0]

        for item in rank_list:
            item_string = item.contents[0].strong.string
            if 'place' in item_string.lower():
                # get place
                deck['rank'] = item_string[6:]
