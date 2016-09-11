ScrapyDouban
================================

豆瓣电影/豆瓣读书 Scarpy 爬虫，实现封面下载+元数据抓取+评论入库。

依赖
-------

    scrapy
    torndb
    arrow


使用
-------

    $ git clone https://github.com/poem/ScrapyDouban.git
    $ cd ScrapyDouban
    $ cd movie/book
    $ scrapy crawl subject
    $ scrapy crawl meta
    $ scrapy crawl comment


注：请导入 douban.sql 到数据库后，自行配置项目下面的 database.py 文件
