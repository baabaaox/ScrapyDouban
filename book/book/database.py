#!/usr/bin/env python
# -*- coding: utf-8 -*-

import torndb

MYSQL_DB = 'douban'
MYSQL_USER = 'user'
MYSQL_PASS = 'pass'
MYSQL_HOST = 'localhost:3306'

conn = torndb.Connection(host=MYSQL_HOST, database=MYSQL_DB, user=MYSQL_USER,
                         password=MYSQL_PASS, max_idle_time=30)
