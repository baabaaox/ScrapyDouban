ScrapyDouban
================================

基于 Python3 的豆瓣电影/豆瓣读书 Scarpy 爬虫，实现封面下载+元数据抓取+评论入库+IP 代理池。

维护这个项目的目的是分享一下我使用 Scrapy 过程中的一些实践，这个项目大概涵盖了 80% 我在使用 Scrapy 过程中的知识点，希望能帮助到正在学习 Scrapy 的朋友，也希望各位在阅读 Scrapy 官方文档后食用。

![Ubuntu](https://assets.ubuntu.com/v1/8dd99b80-ubuntu-logo14.png)
![MySQL](https://www.mysql.com/common/logos/powered-by-mysql-167x86.png)
![Python3](https://www.python.org/static/community_logos/python-powered-w-200x80.png)
![Docker](https://www.docker.com/sites/default/files/horizontal.png)

Python3
-------

对于一个热爱编程的人来说，我们不应该激进，但是也不能停留在过去，今年开始我已经把我所有的 Python 项目迁移到 Python3。

Docker
-------

Ubuntu 容器基于 ubuntu:18.04，默认安装的 Python3 库： scrapy pymysql requests pillow arrow scylla，默认共享 /srv 工作目录，默认共享 8899 Scylla 管理界面端口，默认运行 Scylla 代理池。

MySQL 容器基于 mysql:5.7，默认共享 3306 端口。

SQL
------

请导入 douban.sql 表结构到数据库后，自行配置项目下面的 scrapy/douban/database.py 文件，默认使用的是 docker-compose.yml 里面的配置。

依赖
-------

    scrapy
    pymysql
    pillow
    arrow

流程
-------

    首先收集对于的 Subject ID --> 通过 Subject ID 抓取对应详情页面，收集对应元数据 --> 根据 Subject 来收集评论

使用
-------

    $ git clone https://github.com/poem/ScrapyDouban.git
    $ cd ScrapyDouban/scrapy
    # 抓取电影数据
    $ scrapy crawl movie_subject # 收集电影 ID
    $ scrapy crawl movie_meta # 收集电影元数据
    $ scrapy crawl movie_comment 收集电影评论
    # 抓取书籍数据
    $ scrapy crawl movie_subject # 收集书籍 ID
    $ scrapy crawl movie_meta # 收集书籍元数据
    $ scrapy crawl movie_comment # 收集书籍评论

抓取频率
--------

由于豆瓣的反爬虫机制，现在只能通过代理 IP 来绕过。Docker 容器里面配置好了一个很好的代理池：[Scylla](https://github.com/imWildCat/scylla)，但是需要自己手动在 settings.py 里面启用 douban.middlewares.ProxyMiddleware 中间件，并且由于 Scylla 代理池的 IP 来源于网上公开的代理发布网站，所有很有可能其中很多 IP 已经被 ban 掉，会返回 405 结果，加进去更多是为了展示 Scrapy 代理 IP 的工作流程，如果你真的需要使用豆瓣的数据来进行一些研究，那么你可以去使用一些付费的代理池，这样效果号很多。


图片下载
--------

douban.pipelines.CoverPipeline 已经针对 spider.name 进行过滤，并且修改了保存文件的路径。

注：如果你在收集 subject 的时候出现类似下面 INFO 信息，那么你需要在服务器上 curl 访问一下对应 script 生成的 url 来通过豆瓣的检测机制。

    https://movie.douban.com/subject/26593061/
    <script>var d=[navigator.platform,navigator.userAgent,navigator.vendor].join("|");window.location.href="https://sec.douban.com/a?c=3d001f&d="+d+"&r=https%3A%2F%2Fmovie.douban.com%2Fsubject%2F26590960%2F";</script>
