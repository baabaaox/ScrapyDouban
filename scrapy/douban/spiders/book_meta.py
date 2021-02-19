import douban.database as db
import douban.util as util
from douban.items import BookMeta
from scrapy import Spider

cursor = db.connection.cursor()


class BookMetaSpider(Spider):
    name = "book_meta"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                  (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36"
    allowed_domains = ["book.douban.com"]
    sql = 'SELECT * FROM subjects WHERE type="book" AND douban_id NOT IN \
           (SELECT douban_id FROM books) ORDER BY douban_id'
    cursor.execute(sql)
    books = cursor.fetchall()
    start_urls = ("https://book.douban.com/subject/%s/" % i["douban_id"] for i in books)

    def set_douban_id(self, meta, response):
        meta["douban_id"] = response.url[32:-1]
        return meta

    def set_cover(self, meta, response):
        regex = '//img[@rel="v:photo"]/@src'
        match = response.xpath(regex).get()
        if match:
            if match.find("default") == -1:
                meta["cover"] = match.replace("spst", "lpst").replace("mpic", "lpic")
            else:
                meta["cover"] = ""
        return meta

    def set_slug(self, meta, response):
        meta["slug"] = util.shorturl(meta["douban_id"])
        return meta

    def set_name(self, meta, response):
        regex = "//title/text()"
        match = response.xpath(regex).get()
        if match:
            meta["name"] = match[:-5].strip()
        return meta

    def set_alt_name(self, meta, response):
        regex = '//text()[preceding-sibling::span[text()="原作名:"]][following\
-sibling::br]'
        match = response.xpath(regex).get()
        if match:
            meta["alt_name"] = match
        return meta

    def set_sub_name(self, meta, response):
        regex = '//text()[preceding-sibling::span[text()="副标题:"]][following\
-sibling::br]'
        match = response.xpath(regex).get()
        if match:
            meta["sub_name"] = match
        return meta

    def set_author(self, meta, response):
        regex = '//a[parent::span[child::span[text()=" 作者"]]]/text()'
        matches = response.xpath(regex).getall()
        if matches:
            meta["authors"] = "/".join((i.strip() for i in matches))
        return meta

    def set_summary(self, meta, response):
        regex = '//div[@id="link-report"]//div[@class="intro"]'
        matches = response.xpath(regex)
        if matches:
            items = matches[-1].xpath("p/text()").getall()
            meta["summary"] = "".join(("<p>%s</p>" % i for i in items))
        return meta

    def set_author_intro(self, meta, response):
        regex = '//div[@class="indent "]//div[@class="intro"]'
        matches = response.xpath(regex)
        if matches:
            items = matches[-1].xpath("p/text()").getall()
            meta["author_intro"] = "".join(("<p>%s</p>" % i for i in items))
        return meta

    def set_translator(self, meta, response):
        regex = '//a[parent::span[child::span[text()=" 译者"]]]/text()'
        matches = response.xpath(regex).getall()
        if matches:
            meta["translators"] = "/".join((i.strip() for i in matches))
        return meta

    def set_series(self, meta, response):
        regex = '//a[preceding-sibling::span[text()="丛书:"]][following\
-sibling::br]/text()'
        matches = response.xpath(regex).getall()
        if matches:
            meta["series"] = "/".join((i.strip() for i in matches))
        return meta

    def set_publisher(self, meta, response):
        regex = '//text()[preceding-sibling::span[text()="出版社:"]][following\
-sibling::br]'
        match = response.xpath(regex).get()
        if match:
            meta["publisher"] = match
        return meta

    def set_publish_date(self, meta, response):
        regex = '//text()[preceding-sibling::span[text()="出版年:"]][following\
-sibling::br]'
        match = response.xpath(regex).get()
        if match:
            meta["publish_date"] = match
        return meta

    def set_pages(self, meta, response):
        regex = '//text()[preceding-sibling::span[text()="页数:"]][following\
-sibling::br]'
        match = response.xpath(regex).get()
        if match:
            meta["pages"] = match
        return meta

    def set_price(self, meta, response):
        regex = '//text()[preceding-sibling::span[text()="定价:"]][following\
-sibling::br]'
        match = response.xpath(regex).get()
        if match:
            meta["price"] = match
        return meta

    def set_binding(self, meta, response):
        regex = '//text()[preceding-sibling::span[text()="装帧:"]][following\
-sibling::br]'
        match = response.xpath(regex).get()
        if match:
            meta["binding"] = match
        return meta

    def set_isbn(self, meta, response):
        regex = '//text()[preceding-sibling::span[text()="ISBN:"]][following\
-sibling::br]'
        match = response.xpath(regex).get()
        if match:
            meta["isbn"] = match
        return meta

    def set_score(self, meta, response):
        regex = '//strong[@property="v:average"]/text()'
        match = response.xpath(regex).get()
        if match:
            score = match.strip()
            if score:
                meta["douban_score"] = score
        return meta

    def set_votes(self, meta, response):
        regex = '//span[@property="v:votes"]/text()'
        match = response.xpath(regex).get()
        if match:
            votes = match.strip()
            if votes:
                meta["douban_votes"] = votes
        return meta

    def set_tags(self, meta, response):
        regex = '//a[@class="  tag"]/text()'
        matches = response.xpath(regex).getall()
        if matches:
            meta["tags"] = "/".join((i.strip() for i in matches))
        return meta

    def parse(self, response):
        meta = BookMeta()
        self.set_douban_id(meta, response)
        self.set_cover(meta, response)
        self.set_name(meta, response)
        self.set_sub_name(meta, response)
        self.set_alt_name(meta, response)
        self.set_summary(meta, response)
        self.set_author(meta, response)
        self.set_author_intro(meta, response)
        self.set_translator(meta, response)
        self.set_series(meta, response)
        self.set_publisher(meta, response)
        self.set_publish_date(meta, response)
        self.set_pages(meta, response)
        self.set_price(meta, response)
        self.set_binding(meta, response)
        self.set_isbn(meta, response)
        self.set_score(meta, response)
        self.set_votes(meta, response)
        self.set_tags(meta, response)
        self.set_slug(meta, response)
        return meta
