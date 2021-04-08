## ScrapyDouban

[![ScrapyDouban Demo](https://img.youtube.com/vi/Fyrvrb0rqvE/0.jpg)](https://www.youtube.com/watch?v=Fyrvrb0rqvE) [演示视频](https://www.youtube.com/watch?v=Fyrvrb0rqvE)

基于 Python3 的豆瓣电影/豆瓣读书 Scarpy 爬虫，实现封面下载+元数据抓取+评论入库。

维护这个项目的目的是分享一些我在使用 Scrapy 过程中的实践，该项目大概涵盖了 80% 我所使用到的 Scrapy 知识，希望能帮助到正在学习 Scrapy 的朋友，也希望大家在阅读[ Scrapy 官方文档](https://scrapy.readthedocs.io/en/stable/index.html)后食用，但是请注意目前项目所使用版本为 Scrapy 2.4.1。

![Python3](https://www.python.org/static/community_logos/python-powered-w-200x80.png)
![MySQL](https://www.mysql.com/common/logos/powered-by-mysql-167x86.png)
![Docker](https://www.docker.com/sites/default/files/horizontal.png)

### Docker
-------
项目包含了 douban_scrapyd douban_db douban_adminer 三个容器。

douban_scrapyd 容器基于 [python:3.9-slim-buster](https://pythonspeed.com/articles/base-image-python-docker-images/)，默认安装的 Python3 库有 scrapy scrapyd pymysql pillow arrow，默认映射端口 6800:6800 以方便用户通过宿主机 IP:6800 访问 scrapyd 管理界面，登陆所需参数，用户名:scrapyd 密码:public。

douban_db 容器基于 mysql:8，root 密码为 public，默认初始化时导入 docker/mysql/douban.sql 文件到 douban 数据库。

douban_adminer 容器基于 adminer:4，默认映射端口 8080:8080 以方便用户通过宿主机 IP:8080 访问数据库管理界面，登陆所需参数，服务器:mysql 用户名:root 密码:public。


### 项目 SQL
------

项目所使用的 SQL 文件存放路径为 docker/mysql/douban.sql 。

### 收集流程
-------

    首先收集 Subject ID --> 然后通过 Subject ID 抓取详情页面，收集元数据 --> 最后通过 Subject ID 来收集评论

### 使用方法
-------
    $ git clone https://github.com/baabaaox/ScrapyDouban.git
    # 构建并运行容器
    $ cd ./ScrapyDouban/docker
    $ sudo docker-compose up --build -d
    # 进入 douban_scrapyd 容器
    $ sudo docker exec -it douban_scrapyd bash
    # 进入 scrapy 目录
    $ cd /srv/ScrapyDouban/scrapy
    $ scrapy list
    # 抓取电影数据
    $ scrapy crawl movie_subject # 收集电影 Subject ID
    $ scrapy crawl movie_meta # 收集电影元数据
    $ scrapy crawl movie_comment # 收集电影评论
    # 抓取书籍数据
    $ scrapy crawl book_subject # 收集书籍 Subject ID
    $ scrapy crawl book_meta # 收集书籍元数据
    $ scrapy crawl book_comment # 收集书籍评论

如果你想在测试的时候比较方便的修改代码，你可以把项目所在路径 scrapy 目录挂载到 douban_scrapyd 容器。
如果你习惯使用 scrapyd 进行操作，可以通过 scrapyd-client 直接将项目部署到 douban_scrapyd 容器。

### 代理 IP
--------

由于豆瓣的反爬虫机制，现在只能通过代理 IP 来绕过。默认 settings.py 里面并未启用 douban.middlewares.ProxyMiddleware 中间件，如果你真的需要使用豆瓣的数据来进行一些研究，可以去租用付费的代理池。


### 图片下载
--------

douban.pipelines.CoverPipeline 通过对 spider.name 进行过滤来处理封面下载逻辑，所下载图片文件的保存路径为 douban_scrapy 容器的 /srv/ScrapyDouban/storage 目录。
