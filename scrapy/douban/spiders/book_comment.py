import json

import douban.database as db
from douban.items import Comment
from scrapy import Request, Spider

cursor = db.connection.cursor()


class BookCommentSpider(Spider):
    name = "book_comment"
    allowed_domains = ["book.douban.com"]

    def start_requests(self):
        sql = "SELECT douban_id FROM books WHERE douban_id NOT IN \
            (SELECT douban_id FROM comments GROUP BY douban_id) ORDER BY douban_id DESC"
        cursor.execute(sql)
        books = cursor.fetchall()
        baseurl = "https://m.douban.com/rexxar/api/v2/book/%s/interests?count=5&order_by=hot"
        referer = "https://m.douban.com/book/subject/%s/?from=showing"
        for book in books:
            yield Request(
                baseurl % book["douban_id"], headers={"Referer": referer % book["douban_id"]},
            )

    def parse(self, response):
        douban_id = response.url.split("/")[-2]
        items = json.loads(response.body)["interests"]
        for item in items:
            comment = Comment()
            comment["douban_id"] = douban_id
            comment["douban_comment_id"] = item["id"]
            comment["douban_user_nickname"] = item["user"]["name"]
            comment["douban_user_avatar"] = item["user"]["avatar"]
            comment["douban_user_url"] = item["user"]["url"]
            comment["content"] = item["comment"]
            comment["votes"] = item["vote_count"]
            yield comment
