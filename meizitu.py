#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import threading
import multiprocessing
from mongo_queue import MogoQueue
from download import request
from bs4 import BeautifulSoup

SLEEP_TIME = 1
global currentPath
currentPath = os.path.abspath('.')

def mztu_crawler(name):
	srting = 'crawl_queue' + name
	crawl_queue = MogoQueue('meinvxiezhenji', srting) #这个是我们获取URL 的队列
	
	def pageurl_crawler():
		while True:
			try:
				url = crawl_queue.pop()
				print(url)
			except KeyError:
				print('队列没有数据')
				break
			else:
				img_urls = []
				req = request.get(url, 2).text
				title = crawl_queue.pop_title(url)
				mkdir(title)
				max_span = BeautifulSoup(req, 'lxml').find('div', class_ = 'pagenavi').find_all('span')[-2].get_text()
				for page in range(1, int(max_span) + 1):
					page_url = url + '/' + str(page)
					main_image = BeautifulSoup(request.get(page_url, 3).text, 'lxml').find('div', class_='main-image')
					print('sbbbb111',main_image)
					img_url = main_image.find_all('img')[0]['src']
					print('sbbbb222', srting, img_url)
					img_urls.append(img_url)
					save_img(img_url)
					time.sleep(0.5)
				crawl_queue.complete(url)
				##img_queue.push_imgurl(title, img_urls)
                ##print('插入数据库成功')

	def mkdir(path):
		path = path.strip()
		mypath = os.path.join(currentPath,'meizi')
		isExists = os.path.exists(os.path.join(mypath,path))
		if not isExists:
			os.makedirs(os.path.join(mypath,path))
			os.chdir(os.path.join(mypath,path))
			return True
		else:
			os.chdir(os.path.join(mypath,path))
			return False


	def save_img(image_url):
			name = image_url[-9:]
			img = request.get(image_url,5)
			f = open(name,'ab')
			f.write(img.content)
			f.close()
			print('保存完毕:%s' % (image_url))

	pageurl_crawler()


	# threads = []
	# while threads or crawl_queue:
	# 	'''
	# 	这儿crawl_queue用上了，就是我们__bool__函数的作用，为真则代表我们MongoDB队列里面还有数据
	#         threads 或者 crawl_queue为真都代表我们还没下载完成，程序就会继续执行
	# 	'''
	# 	for thread in threads:
	# 		if not thread.is_alive():#is_alive 是判断是否为空，不是空队列则在队列中删掉
	# 			threads.remove(thread)
	
	# 	while len(threads) < max_threads or crawl_queue.peek():###线程池中的线程少于max_threads 或者 crawl_qeue时
	# 		thread = threading.Thread(target = pageurl_crawler)#创建线程
	# 		thread.setDaemon(True) ##设置守护线程
	# 		thread.start() #启动线程
	# 		threads.append(thread)##添加进线程队列
	# 	time.sleep(SLEEP_TIME)

def process_crawler():
	process = []
	num_cpus = multiprocessing.cpu_count()
	print('将启动进程数为：', num_cpus)
	for i in range(num_cpus):
		time.sleep(SLEEP_TIME)
		p = multiprocessing.Process(target = mztu_crawler, args = [str(i),]) #创建进程
		p.start() #启动进程
		process.append(p) #添加进程队列
	for p in process:
		p.join() #等待进程队列里面的进程结束


if __name__ == '__main__':
	process_crawler()

















