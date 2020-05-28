#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import string

from douban.items import Subject

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Request, Rule


class BookSubjectSpider(CrawlSpider):
    name = 'book_subject'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
    allowed_domains = ['book.douban.com']
    start_urls = ['https://book.douban.com/subject/26628811/']
    rules = (Rule(
        LinkExtractor(allow=('https://book.douban.com/subject/(\\d)+/$')),
        callback='parse_item',
        follow=True,
        process_request='cookie'), )

    def cookie(self, request, response):
        bid = ''.join(
            random.choice(string.ascii_letters + string.digits)
            for x in range(11))
        request.cookies['bid'] = bid
        request = request.replace(url=request.url.replace('?', '/?'))
        return request

    def start_requests(self):
        for url in self.start_urls:
            bid = ''.join(
                random.choice(string.ascii_letters + string.digits)
                for x in range(11))
            yield Request(url, cookies={'bid': bid})

    def get_douban_id(self, subject, response):
        subject['douban_id'] = response.url[32:-1]
        return subject

    def parse_item(self, response):
        subject = Subject()
        self.get_douban_id(subject, response)
        subject['type'] = 'book'
        return subject
