#!/usr/bin/env python3
import requests
import re
import random
import time
from bs4 import BeautifulSoup

class Download(object):
	"""docstring for Download"""
	def __init__(self):
		# super(Download, self).__init__()
		self.user_agent_list = [
			"Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
 			"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
 			"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
 			"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
 			"Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
 			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
 			"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
 			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
 			"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
 			"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
 			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
 			"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
 			"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
 			"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
 			"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
		]
		self.iplist = []
		headers = {'User-Agent':random.choice(self.user_agent_list)}
		try:
			html = requests.get('http://www.66ip.cn/areaindex_19/index.html',headers = headers)
			# iplistn = re.findall(r'r/>(.*?)<b',html.text,re.S)  ##表示从html.text中获取所有r/><b中的内容，re.S的意思是包括匹配包括换行符，findall返回的是个list哦！				
			html_soup = BeautifulSoup(html.text, 'lxml')
			div = html_soup.find('div',id = 'footer').find('div',align = 'center')
			table = div.find('table')
			array = table.find_all('tr')
			array.pop(0)
			for tr in array:
				arr_td = tr.find_all('td')
				dic = {'ip':arr_td[0].get_text(), 'port':arr_td[1].get_text()}
				self.iplist.append(dic)
			# print(self.iplist)
			# for ip in iplistn:
			# 	i = re.sub('\n','',ip)#re.sub 是re模块替换的方法，这儿表示将\n替换为空
			# 	print(i.strip())
			# 	self.iplist.append(i.strip())
		except :
			print('error')
			self.iplist = None

	def get(self,url,timeout,proxy = None,num_reties = 6):
		UA = random.choice(self.user_agent_list)
		headers = {'User-Agent':UA}
		if proxy == None: #代理为空时
			try:
				return requests.get(url,headers = headers,timeout = timeout)
			except:
				if num_reties>0:
					time.sleep(10)#延迟10s
					print('获取网页出错，10s后获取倒数第%s次' % (num_reties))
					return self.get(url,timeout,None,num_reties-1)
				elif len(self.iplist):
					print('开始使用代理')
					time.sleep(10)
					dic = random.choice(self.iplist)
					IP = ''.join(str(dic['ip']).strip())
					PORT = ''.join(str(dic['port']).strip())
					IPPORT = '%s:%s' %(IP,PORT)
					proxy = {'http':IPPORT}
					return self.get(url,timeout,proxy,6)

		else: #当代理不为空时
			try:
				if not isinstance(proxy,dict) and len(self.iplist):
					dic = random.choice(self.iplist)
					IP = ''.join(str(dic['ip']).strip())
					PORT = ''.join(str(dic['port']).strip())
					IPPORT = '%s:%s' %(IP,PORT)
					proxy = {'http':IPPORT}
				print('正在使用代理:%s' %(proxy))
				response = requests.get(url,headers = headers,proxies = proxy,timeout = timeout)
				return response
			except:
				if num_reties>0 and len(self.iplist):
					time.sleep(10)
					dic = random.choice(self.iplist)
					IP = ''.join(str(dic['ip']).strip())
					PORT = ''.join(str(dic['port']).strip())
					IPPORT = '%s:%s' %(IP,PORT)
					proxy = {'http':IPPORT}
					print('正在更换代理，10s后将重新启动获取倒数第%s次' % (num_reties))
					print('当前代理是%s' % (proxy))
					return self.get(url,timeout,proxy,num_reties-1)
				else:
					print('代理不好使了！取消代理')
					return self.get(url,3)


request = Download()






