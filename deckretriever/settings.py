# -*- coding: utf-8 -*-

# Scrapy settings for deckretriever project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'deckretriever'

ITEM_PIPELINES = {
    'deckretriever.pipelines.StandardPipeline': 0
}
SPIDER_MODULES = ['deckretriever.spiders']
# SPIDER_MIDDLEWARES = {
#     'deckretriever.middlewares.DeckMiddleware': 0
# }
NEWSPIDER_MODULE = 'deckretriever.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'deckretriever (+http://www.yourdomain.com)'
DOWNLOAD_DELAY = 0.5
