FROM alpine:3.8

RUN echo -e 'http://mirrors.aliyun.com/alpine/v3.8/main/\nhttp://mirrors.aliyun.com/alpine/v3.8/community/' > /etc/apk/repositories

RUN apk add --update --no-cache gcc musl-dev libffi-dev libxml2-dev libxslt-dev jpeg-dev curl-dev make python3 python3-dev tzdata git curl \
&& cp /usr/share/zoneinfo/Asia/Chongqing /etc/localtime && echo 'Asia/Chongqing' > /etc/timezone && apk del tzdata \
&& python3 -m pip install -i https://mirrors.aliyun.com/pypi/simple/ --upgrade pip \
&& python3 -m pip install -i https://mirrors.aliyun.com/pypi/simple/ scrapy pymysql pillow arrow scylla \
&& git clone https://github.com/40robber/ScrapyDouban.git /srv/ScrapyDouban

CMD ["scylla"]
