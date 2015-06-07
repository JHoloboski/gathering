from scrapy.http.request import Request
from deckretriever.items import EventItem


class DeckMiddleware(object):
    def process_spider_output(self, response, result, spider):
        for x in result:
            print "here is the result:"
            print x
        if isinstance(result, EventItem):
            return Request(
                "http://mtgdecks.net/events/viewByFormat/" + str(result.id)
            )
        else:
            return result
