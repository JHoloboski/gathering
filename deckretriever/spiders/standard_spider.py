# -*- coding: utf-8 -*-
from scrapy.spider import Spider
from scrapy.contrib.spiders import CrawlSpider

from bs4 import BeautifulSoup

from deckretriever.items import EventItem


class StandardSpider(Spider):
    name = 'standard_spider'
    allowed_domains = ['mtgdecks.net']
    start_urls = (
        'http://www.mtgdecks.net/events/viewByFormat/37/',
    )

    def parse(self, response):
        print response.body
        return
        soup = BeautifulSoup(response.body)
        table = soup.select('table:first')
        if not table:
            print 'No tables found on page'

        table = table[0]
        max_id = 0
        _type = None
        _name = None
        for row in table.select('tr'):
            cols = row.select('td')
            if not cols:
                continue
            id, name, type = cols[:3]
            # flake8: noqa
            id, name, type = id.string.strip(), name.string.strip(), type.string.strip()
            if type != 'Standard':
                continue

            max_id = max(id, max_id)
            if max_id == id:
                _type = type
                _name = name

        return EventItem(id=max_id, name=_name, type=_type)


class DeckSpider(CrawlSpider):
    name = 'deck_spider'
    allowed_domains = ['mtgdecks.net']
    start_urls = (
    )

    def parse(self, response):
        pass
