FROM ubuntu:18.04

COPY sources.list /etc/apt/sources.list

RUN apt-get update \
&& apt-get install -y python3-dev python3-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev libcurl4-openssl-dev vim screen cron curl \
&& python3 -m pip install -i https://pypi.doubanio.com/simple/ --upgrade pip \
&& python3 -m pip install -i https://pypi.doubanio.com/simple/ scrapy pymysql requests pillow arrow scylla

CMD ["scylla"]
