# -*- coding: utf-8 -*-

# Scrapy settings for deckgatherer project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'deckgatherer'

SPIDER_MODULES = ['deckgatherer.spiders']
NEWSPIDER_MODULE = 'deckgatherer.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'deckgatherer (+http://www.yourdomain.com)'
DOWNLOAD_DELAY = 0.5
ITEM_PIPELINES = {
    'deckgatherer.pipelines.DeckgathererPipeline': 0
}
