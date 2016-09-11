#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
import random

from book.items import Subject
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class SubjectSpider(CrawlSpider):
    name = 'subject'
    allowed_domains = ['m.douban.com']
    start_urls = ['https://m.douban.com/book/subject/26856953/?refer=home']
    rules = (
        Rule(LinkExtractor(allow=('book/subject/(\d).*rec$')),
             callback='parse_item', follow=True, process_request='cookie'),
    )

    def cookie(self, request):
        bid = ''.join(random.choice(string.ascii_letters + string.digits) for
                      x in range(11))
        request.cookies['bid'] = bid
        return request

    def make_requests_from_url(self, url):
        request = super(SubjectSpider, self).make_requests_from_url(url)
        bid = ''.join(random.choice(string.ascii_letters + string.digits) for
                      x in range(11))
        request.cookies['bid'] = bid
        return request

    def get_douban_id(self, subject, response):
        subject['douban_id'] = response.url[34:-10]
        return subject

    def parse_item(self, response):
        subject = Subject()
        self.get_douban_id(subject, response)
        subject['type'] = 'book'
        return subject
