FROM baabaaox/scrapy:2.4.1-alpine

RUN apk add --update --no-cache jpeg-dev tzdata git \
&& cp /usr/share/zoneinfo/Asia/Chongqing /etc/localtime && echo 'Asia/Chongqing' > /etc/timezone && apk del tzdata \
&& pip install -i https://mirrors.aliyun.com/pypi/simple/ --upgrade pip \
&& pip install -i https://mirrors.aliyun.com/pypi/simple/ pymysql==1.0.2 pillow==8.1.0 arrow==0.17.0 \
&& pip install -U git+https://github.com/scrapy/scrapyd.git \
&& git clone https://github.com/baabaaox/ScrapyDouban.git /srv/ScrapyDouban

COPY scrapyd.conf /etc/scrapyd/

EXPOSE 6800

CMD ["scrapyd"]
