FROM alpine:3.11

RUN echo -e 'http://mirrors.aliyun.com/alpine/v3.11/main/\nhttp://mirrors.aliyun.com/alpine/v3.11/community/' > /etc/apk/repositories

RUN apk add --update --no-cache gcc musl-dev libffi-dev libxml2-dev libxslt-dev jpeg-dev curl-dev make python3 python3-dev tzdata git curl \
&& cp /usr/share/zoneinfo/Asia/Chongqing /etc/localtime && echo 'Asia/Chongqing' > /etc/timezone && apk del tzdata \
&& python3 -m pip install -i https://mirrors.aliyun.com/pypi/simple/ --upgrade pip \
&& python3 -m pip install -i https://mirrors.aliyun.com/pypi/simple/ scrapy==2.1.0 pymysql==0.9.3 pillow==7.1.2 arrow==0.15.6 \
&& git clone https://github.com/baabaaox/ScrapyDouban.git /srv/ScrapyDouban
