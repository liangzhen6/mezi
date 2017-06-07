#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from mongo_queue import MogoQueue
from bs4 import BeautifulSoup
from download import request
import multiprocessing

num_cpus = multiprocessing.cpu_count()
spider_allqueue = []
for x in range(num_cpus):
	string = 'crawl_queue' + str(x)
	spider_queue = MogoQueue('meinvxiezhenji', string)
	spider_allqueue.append(spider_queue)

def start(url):
	response = request.get(url, 3)
	Soup = BeautifulSoup(response.text, 'lxml')
	all_div = Soup.find('div', class_ = 'all')
	all_ul = all_div.find_all('ul', class_ = 'archives')
	all_a = all_ul[0].find_all('a')
	for index,a in enumerate(all_a):
		title = a.get_text()
		url = a['href']
		spider_queue = spider_allqueue[index%num_cpus]
		print(spider_queue)
		spider_queue.push(url, title)


if __name__ == '__main__':
	start('http://www.mzitu.com/all/')

