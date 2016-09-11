#!/usr/bin/env python
# -*- coding: utf-8 -*-

BOT_NAME = 'book'

SPIDER_MODULES = ['book.spiders']
NEWSPIDER_MODULE = 'book.spiders'

IMAGES_STORE = '../storage/book/'

COOKIES_ENABLED = True
COOKIE_DEBUG = True
LOG_LEVEL = 'INFO'
# LOG_LEVEL = 'DEBUG'
CONCURRENT_REQUESTS = 100
CONCURRENT_REQUESTS_PER_DOMAIN = 1000

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, \
like Gecko) Chrome/49.0.2623.87 Safari/537.36"


DEFAULT_REQUEST_HEADERS = {
    'Referer': 'https://m.douban.com/book/'
}

ITEM_PIPELINES = {
    'book.pipelines.CoverPipeline': 0,
    'book.pipelines.BookPipeline': 1,
}
