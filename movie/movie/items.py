#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy import Item, Field


class Subject(Item):
    douban_id = Field()
    type = Field()


class Meta(Item):
    douban_id = Field()
    type = Field()
    cover = Field()
    name = Field()
    slug = Field()
    year = Field()
    directors = Field()
    actors = Field()
    genres = Field()
    official_site = Field()
    regions = Field()
    languages = Field()
    release_date = Field()
    mins = Field()
    alias = Field()
    imdb_id = Field()
    douban_id = Field()
    douban_score = Field()
    douban_votes = Field()
    tags = Field()
    storyline = Field()


class Comment(Item):
    douban_id = Field()
    douban_comment_id = Field()
    douban_user_nickname = Field()
    douban_user_avatar = Field()
    douban_user_url = Field()
    content = Field()
    votes = Field()
