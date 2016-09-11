#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import book.database as db

from scrapy import Request
from scrapy.utils.misc import arg_to_iter
from twisted.internet.defer import DeferredList
from scrapy.pipelines.images import ImagesPipeline
from book.items import Subject, Meta, Comment


class BookPipeline(object):
    def get_subject(self, item):
        sql = 'SELECT * FROM subjects WHERE douban_id=%s' % item['douban_id']
        return db.conn.get(sql)

    def save_subject(self, item):
        keys = item.keys()
        values = item.values()
        fields = ','.join(keys)
        temp = ','.join(['%s'] * len(keys))
        sql = 'INSERT INTO subjects (%s) VALUES (%s)' % (fields, temp)
        db.conn.insert(sql, *values)

    def get_meta(self, item):
        sql = 'SELECT * FROM books WHERE douban_id=%s' % item['douban_id']
        return db.conn.get(sql)

    def save_meta(self, item):
        keys = item.keys()
        values = item.values()
        fields = ','.join(keys)
        temp = ','.join(['%s'] * len(keys))
        sql = 'INSERT INTO books (%s) VALUES (%s)' % (fields, temp)
        db.conn.insert(sql, *(i.strip() for i in values))

    def update_meta(self, item):
        douban_id = item.pop('douban_id')
        keys = item.keys()
        values = item.values()
        values.append(douban_id)
        fields = ['%s=' % i + '%s' for i in keys]
        sql = 'UPDATE books SET %s WHERE douban_id=%s\
' % (','.join(fields), '%s')
        db.conn.update(sql, *values)

    def get_comment(self, item):
        sql = 'SELECT * FROM comments WHERE douban_comment_id=%s\
' % item['douban_comment_id']
        return db.conn.get(sql)

    def save_comment(self, item):
        keys = item.keys()
        values = item.values()
        fields = ','.join(keys)
        temp = ','.join(['%s'] * len(keys))
        db.conn.execute('SET NAMES utf8mb4')
        sql = 'INSERT INTO comments (%s) VALUES (%s)' % (fields, temp)
        db.conn.insert(sql, *(i.strip() for i in values))

    def process_item(self, item, spider):
        if isinstance(item, Subject):
            '''
            subject
            '''
            exsit = self.get_subject(item)
            if not exsit:
                self.save_subject(item)
        elif isinstance(item, Meta):
            '''
            book meta
            '''
            exsit = self.get_meta(item)
            if not exsit:
                try:
                    self.save_meta(item)
                except Exception, e:
                    print item
                    print e
            else:
                self.update_meta(item)

        elif isinstance(item, Comment):
            '''
            book comment
            '''
            exsit = self.get_comment(item)
            if not exsit:
                try:
                    self.save_comment(item)
                except Exception, e:
                    print item
                    print e
        return item


class CoverPipeline(ImagesPipeline):
    def process_item(self, item, spider):
        if spider.name != 'meta':
            return item
        info = self.spiderinfo
        requests = arg_to_iter(self.get_media_requests(item, info))
        dlist = [self._process_request(r, info) for r in requests]
        dfd = DeferredList(dlist, consumeErrors=1)
        return dfd.addCallback(self.item_completed, item, info)

    def file_path(self, request, response=None, info=None):
        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('ImagesPipeline.image_key(url) and file_key(url) methods are \
deprecated, please use file_path(request, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)
        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url
        if not hasattr(self.file_key, '_base'):
            _warn()
            return self.file_key(url)
        elif not hasattr(self.image_key, '_base'):
            _warn()
            return self.image_key(url)
        image_guid = hashlib.sha1(url).hexdigest()
        return '%s%s/%s%s/%s.jpg\
' % (image_guid[9], image_guid[19], image_guid[29], image_guid[39], image_guid)

    def get_media_requests(self, item, info):
        if item['cover']:
            return Request(item['cover'])

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if image_paths:
            item['cover'] = image_paths[0]
        else:
            item['cover'] = ''
        return item
