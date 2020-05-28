#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql

MYSQL_DB = 'douban'
MYSQL_USER = 'root'
MYSQL_PASS = 'HardM0de'
MYSQL_HOST = 'db'

connection = pymysql.connect(host=MYSQL_HOST,
                             user=MYSQL_USER,
                             password=MYSQL_PASS,
                             db=MYSQL_DB,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
