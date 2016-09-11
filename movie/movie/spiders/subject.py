#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
import random

from movie.items import Subject
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class SubjectSpider(CrawlSpider):
    name = 'subject'
    allowed_domains = ['wap.douban.com']
    url = 'https://wap.douban.com/movie/top250/?page=%s'
    start_urls = [url % i for i in range(1, 11)]
    rules = (
        Rule(LinkExtractor(allow=('movie/subject/(\d)*/$')),
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
        subject['douban_id'] = response.url[37:-1]
        return subject

    def parse_item(self, response):
        subject = Subject()
        self.get_douban_id(subject, response)
        subject['type'] = 'movie'
        return subject
