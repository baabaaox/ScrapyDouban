#!/usr/bin/env python
# -*- coding: utf-8 -*-


import string
import random
import book.util as util
import book.database as db

from scrapy import Spider
from book.items import Meta


class MetaSpider(Spider):
    name = 'meta'
    allowed_domains = ["book.douban.com"]
    books = db.conn.query('SELECT * FROM subjects WHERE type="book" AND \
douban_id NOT IN (SELECT douban_id FROM books) ORDER BY douban_id DESC')
    start_urls = (
        'https://book.douban.com/subject/%s/' % i['douban_id'] for i in books
    )

    def make_requests_from_url(self, url):
        request = super(MetaSpider, self).make_requests_from_url(url)
        bid = ''.join(random.choice(string.ascii_letters + string.digits) for
                      x in range(11))
        request.cookies['bid'] = bid
        request.meta['dont_redirect'] = True
        request.meta['handle_httpstatus_list'] = [302]
        return request

    def get_douban_id(self, meta, response):
        meta['douban_id'] = response.url[32:-1]
        return meta

    def get_cover(self, meta, response):
        regx = '//img[@rel="v:photo"]/@src'
        data = response.xpath(regx).extract()
        if data:
            if (data[0].find('default') == -1):
                meta['cover'] = data[0].replace('spst', '\
lpst').replace('mpic', 'lpic')
            else:
                meta['cover'] = ''
        return meta

    def get_slug(self, meta, response):
        meta['slug'] = util.shorturl(meta['douban_id'])
        return meta

    def get_name(self, meta, response):
        regx = '//title/text()'
        data = response.xpath(regx).extract()
        if data:
            meta['name'] = data[0][:-5].strip()
        return meta

    def get_alt_name(self, meta, response):
        regx = u'//text()[preceding-sibling::span[text()="原作名:"]][following\
-sibling::br]'
        data = response.xpath(regx).extract()
        if data:
            meta['alt_name'] = data[0]
        return meta

    def get_sub_name(self, meta, response):
        regx = u'//text()[preceding-sibling::span[text()="副标题:"]][following\
-sibling::br]'
        data = response.xpath(regx).extract()
        if data:
            meta['sub_name'] = data[0]
        return meta

    def get_author(self, meta, response):
        regx = u'//a[parent::span[child::span[text()=" 作者"]]]/text()'
        authors = response.xpath(regx).extract()
        if authors:
            meta['authors'] = '/'.join((i.strip() for i in authors))
        return meta

    def get_summary(self, meta, response):
        regx = '//div[@id="link-report"]//div[@class="intro"]'
        matches = response.xpath(regx)
        if matches:
            items = matches[-1].xpath(u'p/text()').extract()
            meta['summary'] = ''.join(('<p>%s</p>' % i for i in items))

        return meta

    def get_author_intro(self, meta, response):
        regx = '//div[@class="indent "]//div[@class="intro"]'
        matches = response.xpath(regx)
        if matches:
            items = matches[-1].xpath('p/text()').extract()
            meta['author_intro'] = ''.join(('<p>%s</p>' % i for i in items))

        return meta

    def get_translator(self, meta, response):
        regx = u'//a[parent::span[child::span[text()=" 译者"]]]/text()'
        translators = response.xpath(regx).extract()
        if translators:
            meta['translators'] = '/'.join((i.strip() for i in translators))
        return meta

    def get_series(self, meta, response):
        regx = u'//a[preceding-sibling::span[text()="丛书:"]][following\
-sibling::br]/text()'
        series = response.xpath(regx).extract()
        if series:
            meta['series'] = '/'.join((i.strip() for i in series))
        return meta

    def get_publisher(self, meta, response):
        regx = u'//text()[preceding-sibling::span[text()="出版社:"]][following\
-sibling::br]'
        data = response.xpath(regx).extract()
        if data:
            meta['publisher'] = data[0]
        return meta

    def get_publish_date(self, meta, response):
        regx = u'//text()[preceding-sibling::span[text()="出版年:"]][following\
-sibling::br]'
        data = response.xpath(regx).extract()
        if data:
            meta['publish_date'] = data[0]
        return meta

    def get_pages(self, meta, response):
        regx = u'//text()[preceding-sibling::span[text()="页数:"]][following\
-sibling::br]'
        data = response.xpath(regx).extract()
        if data:
            meta['pages'] = data[0]
        return meta

    def get_price(self, meta, response):
        regx = u'//text()[preceding-sibling::span[text()="定价:"]][following\
-sibling::br]'
        data = response.xpath(regx).extract()
        if data:
            meta['price'] = data[0][:-1]
        return meta

    def get_binding(self, meta, response):
        regx = u'//text()[preceding-sibling::span[text()="装帧:"]][following\
-sibling::br]'
        data = response.xpath(regx).extract()
        if data:
            meta['binding'] = data[0]
        return meta

    def get_isbn(self, meta, response):
        regx = '//text()[preceding-sibling::span[text()="ISBN:"]][following\
-sibling::br]'
        data = response.xpath(regx).extract()
        if data:
            meta['isbn'] = data[0]
        return meta

    def get_score(self, meta, response):
        regx = '//strong[@property="v:average"]/text()'
        data = response.xpath(regx).extract()
        if data:
            score = data[0].strip()
            if score:
                meta['douban_score'] = score
        return meta

    def get_votes(self, meta, response):
        regx = '//span[@property="v:votes"]/text()'
        data = response.xpath(regx).extract()
        if data:
            votes = data[0].strip()
            if votes:
                meta['douban_votes'] = votes
        return meta

    def get_tags(self, meta, response):
        regx = '//a[@class="  tag"]/text()'
        tags = response.xpath(regx).extract()
        if tags:
            meta['tags'] = '/'.join((i.strip() for i in tags))
        return meta

    def parse(self, response):
        if 35000 > len(response.body):
            print response.body
            print response.url
        elif 404 == response.status:
            print response.url
        else:
            meta = Meta()
            self.get_douban_id(meta, response)
            self.get_cover(meta, response)
            self.get_name(meta, response)
            self.get_sub_name(meta, response)
            self.get_alt_name(meta, response)
            self.get_summary(meta, response)
            self.get_author(meta, response)
            self.get_author_intro(meta, response)
            self.get_translator(meta, response)
            self.get_series(meta, response)
            self.get_publisher(meta, response)
            self.get_publish_date(meta, response)
            self.get_pages(meta, response)
            self.get_price(meta, response)
            self.get_binding(meta, response)
            self.get_isbn(meta, response)
            self.get_score(meta, response)
            self.get_votes(meta, response)
            self.get_tags(meta, response)
            self.get_slug(meta, response)
            return meta
