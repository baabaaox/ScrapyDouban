import hashlib
import logging

from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.misc import arg_to_iter
from scrapy.utils.python import to_bytes
from twisted.internet.defer import DeferredList

import douban.database as db
from douban.items import BookMeta, Comment, MovieMeta, Subject

cursor = db.connection.cursor()


class DoubanPipeline(object):
    def get_subject(self, item):
        sql = "SELECT id FROM subjects WHERE douban_id=%s" % item["douban_id"]
        cursor.execute(sql)
        return cursor.fetchone()

    def save_subject(self, item):
        keys = item.keys()
        values = tuple(item.values())
        fields = ",".join(keys)
        temp = ",".join(["%s"] * len(keys))
        sql = "INSERT INTO subjects (%s) VALUES (%s)" % (fields, temp)
        cursor.execute(sql, values)
        return db.connection.commit()

    def get_movie_meta(self, item):
        sql = "SELECT id FROM movies WHERE douban_id=%s" % item["douban_id"]
        cursor.execute(sql)
        return cursor.fetchone()

    def save_movie_meta(self, item):
        keys = item.keys()
        values = tuple(item.values())
        fields = ",".join(keys)
        temp = ",".join(["%s"] * len(keys))
        sql = "INSERT INTO movies (%s) VALUES (%s)" % (fields, temp)
        cursor.execute(sql, tuple(i.strip() for i in values))
        return db.connection.commit()

    def update_movie_meta(self, item):
        douban_id = item.pop("douban_id")
        keys = item.keys()
        values = tuple(item.values())
        values.append(douban_id)
        fields = ["%s=" % i + "%s" for i in keys]
        sql = "UPDATE movies SET %s WHERE douban_id=%s" % (",".join(fields), "%s")
        cursor.execute(sql, tuple(i.strip() for i in values))
        return db.connection.commit()

    def get_book_meta(self, item):
        sql = "SELECT id FROM books WHERE douban_id=%s" % item["douban_id"]
        cursor.execute(sql)
        return cursor.fetchone()

    def save_book_meta(self, item):
        keys = item.keys()
        values = tuple(item.values())
        fields = ",".join(keys)
        temp = ",".join(["%s"] * len(keys))
        sql = "INSERT INTO books (%s) VALUES (%s)" % (fields, temp)
        cursor.execute(sql, tuple(i.strip() for i in values))
        return db.connection.commit()

    def update_book_meta(self, item):
        douban_id = item.pop("douban_id")
        keys = item.keys()
        values = tuple(item.values())
        values.append(douban_id)
        fields = ["%s=" % i + "%s" for i in keys]
        sql = "UPDATE books SET %s WHERE douban_id=%s" % (",".join(fields), "%s")
        cursor.execute(sql, values)
        return db.connection.commit()

    def get_comment(self, item):
        sql = "SELECT * FROM comments WHERE douban_comment_id=%s" % item["douban_comment_id"]
        cursor.execute(sql)
        return cursor.fetchone()

    def save_comment(self, item):
        keys = item.keys()
        values = tuple(item.values())
        fields = ",".join(keys)
        temp = ",".join(["%s"] * len(keys))
        sql = "INSERT INTO comments (%s) VALUES (%s)" % (fields, temp)
        cursor.execute(sql, values)
        return db.connection.commit()

    def process_item(self, item, spider):
        try:
            if isinstance(item, Subject):
                """
                subject
                """
                exist = self.get_subject(item)
                if not exist:
                    self.save_subject(item)
            elif isinstance(item, MovieMeta):
                """
                meta
                """
                exist = self.get_movie_meta(item)
                if not exist:
                    self.save_movie_meta(item)
                else:
                    self.update_movie_meta(item)
            elif isinstance(item, BookMeta):
                """
                meta
                """
                exist = self.get_book_meta(item)
                if not exist:
                    self.save_book_meta(item)
                else:
                    self.update_book_meta(item)
            elif isinstance(item, Comment):
                """
                comment
                """
                exist = self.get_comment(item)
                if not exist:
                    self.save_comment(item)
        except Exception as e:
            logging.warn(item)
            logging.error(e)
        return item


class CoverPipeline(ImagesPipeline):
    def process_item(self, item, spider):
        if "meta" not in spider.name:
            return item
        info = self.spiderinfo
        requests = arg_to_iter(self.get_media_requests(item, info))
        dlist = [self._process_request(r, info, item) for r in requests]
        dfd = DeferredList(dlist, consumeErrors=1)
        return dfd.addCallback(self.item_completed, item, info)

    def file_path(self, request, response=None, info=None, *, item=None):
        guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return "%s%s/%s%s/%s.jpg" % (guid[9], guid[19], guid[29], guid[39], guid)

    def get_media_requests(self, item, info):
        if item["cover"]:
            return Request(item["cover"])

    def item_completed(self, results, item, info):
        image_paths = [x["path"] for ok, x in results if ok]
        if image_paths:
            item["cover"] = image_paths[0]
        else:
            item["cover"] = ""
        return item
