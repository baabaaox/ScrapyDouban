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


注：请导入 douban.sql 到数据库后，自行配置项目下面的 database.py 文件。如果你在收集 subject 的时候出现类似下面 INFO 信息，那么你需要在服务器上 curl 访问一下对应 script 生成的 url 来通过豆瓣的检测机制。

    https://movie.douban.com/subject/26593061/
    <script>var d=[navigator.platform,navigator.userAgent,navigator.vendor].join("|");window.location.href="https://sec.douban.com/a?c=3d001f&d="+d+"&r=https%3A%2F%2Fmovie.douban.com%2Fsubject%2F26590960%2F";</script>
