# -*- coding: utf-8 -*-
"""
获取最后时间的数据
"""
from douban import database
from scrapy.utils.project import get_project_settings
settings = dict(get_project_settings().items())
cursor = database.connection.cursor()

def get_book_last_id():
	"""
	获取最后一条豆瓣书籍数据
	:return: int
	"""
	sql = 'SELECT douban_id FROM ' + settings['BOOKS_NAME'] + ' order by id desc limit 1'
	cursor.execute(sql)
	info =  cursor.fetchone()
	if info is None:
		return 26628811

	return info['douban_id']
def get_movie_last_id():
	"""
	获取最后一条电影数据
	:return: int
	"""
	sql = 'SELECT douban_id FROM ' + settings['MOVIES_NAME'] + ' order by id desc limit 1'
	cursor.execute(sql)
	info =  cursor.fetchone()
	if info is None:
		return 1292052

	return info['douban_id']

