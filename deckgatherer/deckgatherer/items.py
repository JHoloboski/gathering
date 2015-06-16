# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EventItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    type = scrapy.Field()


class DeckItem(scrapy.Item):
    name = scrapy.Field()
    raw_deck = scrapy.Field()  # contents of the deck in a file
    rank = scrapy.Field()  # what the deck placed in the event


class TournamentItem(scrapy.Item):
    # Would be nice to store this information, decks can relate
    # back to individual tournaments
    date = scrapy.Field()
    format = scrapy.Field()  # which format of standard
    players = scrapy.Field()  # number of players
