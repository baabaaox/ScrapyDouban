## ScrapyDouban

[![ScrapyDouban Demo](https://img.youtube.com/vi/Yt8_j0TEvh0/0.jpg)](https://www.youtube.com/watch?v=Yt8_j0TEvh0) [演示视频](https://www.youtube.com/watch?v=Yt8_j0TEvh0)

基于 Python3 的豆瓣电影/豆瓣读书 Scarpy 爬虫，实现封面下载+元数据抓取+评论入库+IP 代理池。

维护这个项目的目的是分享一些我在使用 Scrapy 过程中的实践，该项目大概涵盖了 80% 我所使用到的 Scrapy 知识，希望能帮助到正在学习 Scrapy 的朋友，也希望大家在阅读[ Scrapy 官方文档](https://scapy.readthedocs.io/en/stable/index.html)后食用，但是请注意目前项目所使用版本为 Scrapy 1.5.1。

![Python3](https://www.python.org/static/community_logos/python-powered-w-200x80.png)
![MySQL](https://www.mysql.com/common/logos/powered-by-mysql-167x86.png)
![Docker](https://www.docker.com/sites/default/files/horizontal.png)
![Alpine Linux](https://alpinelinux.org/alpinelinux-logo.svg)

### Docker
-------
项目包含了 douban_scrapy douban_db douban_adminer 三个容器。

douban_scrapy 容器基于 alpine:3.8，默认安装的 Python3 库有 scrapy pymysql pillow arrow scylla，默认运行 Scylla 代理池，默认映射端口 8899:8899 以方便用户通过宿主机 IP 访问 Scylla 管理界面。

douban_db 容器基于 mysql:8，root 密码为 HardM0de，默认初始化时导入 docker/mysql/douban.sql 文件到 douban 数据库。

douban_adminer 容器基于 adminer:4，默认映射端口 8080:8080 以方便用户通过宿主机 IP 访问数据库管理界面。


### 项目 SQL
------

项目所使用的 SQL 文件存放路径为 docker/mysql/douban.sql 。

### 收集流程
-------

    首先收集 Subject ID --> 然后通过 Subject ID 抓取详情页面，收集元数据 --> 最后通过 Subject ID 来收集评论

### 使用方法
-------
    $ git clone https://github.com/poem/ScrapyDouban.git
    # 构建并运行容器
    $ cd ./ScrapyDouban/docker
    $ sudo docker-compose up --build -d
    # 进入 douban_scrapy 容器
    $ sudo docker exec -it douban_scrapy ash
    # 进入 scrapy 目录
    $ cd /srv/ScrapyDouban/scrapy
    $ scrapy list
    # 抓取电影数据
    $ scrapy crawl movie_subject # 收集电影 Subject ID
    $ scrapy crawl movie_meta # 收集电影元数据
    $ scrapy crawl movie_comment 收集电影评论
    # 抓取书籍数据
    $ scrapy crawl book_subject # 收集书籍 Subject ID
    $ scrapy crawl book_meta # 收集书籍元数据
    $ scrapy crawl book_comment # 收集书籍评论

### 代理 IP
--------

由于豆瓣的反爬虫机制，现在只能通过代理 IP 来绕过。douban_scrapy 容器里面配置好了一个很好的代理池：[Scylla](https://github.com/imWildCat/scylla)，默认 settings.py 里面并未启用 douban.middlewares.ProxyMiddleware 中间件，因为 Scylla 代理池的 IP 来源于网上公开的代理发布网站，所有一定几率其中的 IP 已经被 ban 掉，这里只是为了展示 Scrapy 代理 IP 的工作流程，如果你真的需要使用豆瓣的数据来进行一些研究，可以去租用付费的代理池。


### 图片下载
--------

douban.pipelines.CoverPipeline 通过对 spider.name 进行过滤来处理封面下载逻辑，所下载图片文件的保存路径为 douban_scrapy 容器的 /srv/ScrapyDouban/storage 目录。

注：如果你在收集 subject 的时候出现类似下面 INFO 信息，那么你需要在服务器上 curl 访问一下对应 script 生成的 url 来通过豆瓣的检测机制。

    https://movie.douban.com/subject/26593061/
    <script>var d=[navigator.platform,navigator.userAgent,navigator.vendor].join("|");window.location.href="https://sec.douban.com/a?c=3d001f&d="+d+"&r=https%3A%2F%2Fmovie.douban.com%2Fsubject%2F26590960%2F";</script>
