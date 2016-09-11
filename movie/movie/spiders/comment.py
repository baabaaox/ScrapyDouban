#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
import random
import movie.database as db

from scrapy import Spider
from movie.items import Comment


class CommentSpider(Spider):
    name = 'comment'
    allowed_domains = ['movie.douban.com']
    movies = db.conn.query('SELECT douban_id FROM movies WHERE douban_id NOT \
IN (SELECT douban_id FROM comments GROUP BY douban_id) ORDER BY douban_id \
DESC')
    start_urls = (
        'https://movie.douban.com/subject/%s/comments\
' % i['douban_id'] for i in movies
    )

    def make_requests_from_url(self, url):
        request = super(CommentSpider, self).make_requests_from_url(url)
        bid = ''.join(random.choice(string.ascii_letters + string.digits) for
                      x in range(11))
        request.cookies['bid'] = bid
        request.meta['dont_redirect'] = True
        request.meta['handle_httpstatus_list'] = [302]
        return request

    def get_douban_id(self, comment, response):
        comment['douban_id'] = response.url[33:-9]
        return comment

    def get_douban_comment_id(self, comment, response):
        regx = '@data-cid'
        matches = response.xpath(regx).extract()
        if matches:
            comment['douban_comment_id'] = matches[0]
        else:
            comment['douban_comment_id'] = '0'
        return comment

    def get_content(self, comment, response):
        regx = 'div[@class="comment"]/p/text()'
        matches = response.xpath(regx).extract()
        if matches:
            comment['content'] = matches[0]
        else:
            comment['content'] = ''
        return comment

    def get_votes(self, comment, response):
        regx = 'div/h3/span/span[@class="votes pr5"]/text()'
        matches = response.xpath(regx).extract()
        if matches:
            comment['votes'] = matches[0]
        else:
            comment['votes'] = '0'
        return comment

    def get_douban_user_nickname(self, comment, response):
        regx = 'div[@class="avatar"]/a/@title'
        matches = response.xpath(regx).extract()
        if matches:
            comment['douban_user_nickname'] = matches[0]
        else:
            comment['douban_user_nickname'] = ''
        return comment

    def get_douban_user_url(self, comment, response):
        regx = 'div[@class="avatar"]/a/@href'
        matches = response.xpath(regx).extract()
        if matches:
            comment['douban_user_url'] = matches[0]
        else:
            comment['douban_user_url'] = ''
        return comment

    def get_douban_user_avatar(self, comment, response):
        regx = 'div[@class="avatar"]/a/img/@src'
        matches = response.xpath(regx).extract()
        if matches:
            comment['douban_user_avatar'] = matches[0]
        else:
            comment['douban_user_avatar'] = ''
        return comment

    def parse(self, response):
        if 302 == response.status:
            print response.url
        else:
            regx = '//div[@class="comment-item"][boolean(@data-cid)]'
            items = response.xpath(regx)
            for item in items:
                comment = Comment()
                self.get_douban_id(comment, response)
                self.get_douban_comment_id(comment, item)
                self.get_douban_user_nickname(comment, item)
                self.get_douban_user_avatar(comment, item)
                self.get_douban_user_url(comment, item)
                self.get_content(comment, item)
                self.get_votes(comment, item)
                yield comment
