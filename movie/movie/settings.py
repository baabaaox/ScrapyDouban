#!/usr/bin/env python
# -*- coding: utf-8 -*-

BOT_NAME = 'movie'

SPIDER_MODULES = ['movie.spiders']
NEWSPIDER_MODULE = 'movie.spiders'

IMAGES_STORE = '../storage/movie/'

COOKIES_ENABLED = True
COOKIE_DEBUG = True
LOG_LEVEL = 'INFO'
# LOG_LEVEL = 'DEBUG'
CONCURRENT_REQUESTS = 100
CONCURRENT_REQUESTS_PER_DOMAIN = 1000

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, \
like Gecko) Chrome/49.0.2623.87 Safari/537.36"


DEFAULT_REQUEST_HEADERS = {
    'Referer': 'https://movie.douban.com/'
}

ITEM_PIPELINES = {
    'movie.pipelines.CoverPipeline': 0,
    'movie.pipelines.MoviePipeline': 1,
}
