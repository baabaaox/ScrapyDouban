FROM python:3.9-slim-buster

ARG SCRAPY_VERSION=2.5.0

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && pip install -i https://mirrors.aliyun.com/pypi/simple/ --upgrade pip \
    && pip install -i https://mirrors.aliyun.com/pypi/simple/ scrapy==$SCRAPY_VERSION pymysql==1.0.2 pillow==8.2.0 arrow==1.0.3 \
    && pip install -U git+https://github.com/scrapy/scrapyd.git \
    && git clone https://github.com/baabaaox/ScrapyDouban.git /srv/ScrapyDouban

COPY scrapyd.conf /etc/scrapyd/

EXPOSE 6800

CMD ["scrapyd"]
