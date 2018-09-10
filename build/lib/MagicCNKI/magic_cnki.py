import os
import random
import time

import cchardet
import requests

from bs4 import BeautifulSoup
from MagicCNKI.config import USER_AGENT


class MagicCNKI():
	"""
	Magic CNKI search.
	"""

	def __init__(self):
		pass

	def search(self, query, start=0, pause=2):
		"""
		Get the results you want,such as title,description,url
		:param query:
		:param start:
		:return: Generator
		"""
		start = start // 15 * 15
		content = self.search_page(query, start, pause)
		soup = BeautifulSoup(content, "html.parser")
		for item in soup.find_all('div', class_='wz_content'):
			result = {}
			result['title'] = item.h3.a.get_text()
			result['url'] = item.h3.a['href']
			result['text'] = item.div.span.get_text()
			result['info'] = item.find('span', class_='year-count').span.get_text()
			result['count'] = item.find('span', class_='count').get_text()
			yield result

	def search_page(self, query, start=0, pause=2):
		"""
		Baidu search
		:param query: Keyword
		:param language: Language
		:return: result
		"""
		start = start // 15 * 15
		time.sleep(pause)
		param = { 'q' : query , 'p': str(start) , 'rank': 'relevant', 'cluster': 'all'}
		url = 'http://search.cnki.net/Search.aspx'
		# Add headers
		headers = { 'User-Agent': self.get_random_user_agent(), 
					'Host': 'search.cnki.net'
					}
		try:
			requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
			r = requests.get(url=url,
							 params=param,
							 headers=headers,
							 allow_redirects=False,
							 verify=False,
							 timeout=10)
			content = r.content
			charset = cchardet.detect(content)
			text = content.decode(charset['encoding'])
			return text
		except:
			return None

	def search_url(self, query, start=0, pause=2):
		"""
		:param query:
		:param start:
		:return: Generator
		"""
		start = start // 15 * 15
		content = self.search_page(query, start, pause)
		soup = BeautifulSoup(content, "html.parser")
		now = start + 1
		for item in soup.find_all('div', class_='wz_content'):
			yield item.h3.a['href']

	def pq_html(self, content):
		"""
		Parsing HTML by pyquery
		:param content: HTML content
		:return:
		"""
		return pq(content)

	def get_random_user_agent(self):
		"""
		Get a random user agent string.
		:return: Random user agent string.
		"""
		return random.choice(self.get_data('user_agents.txt', USER_AGENT))

	def get_data(self, filename, default=''):
		"""
		Get data from a file
		:param filename: filename
		:param default: default value
		:return: data
		"""
		root_folder = os.path.dirname(__file__)
		user_agents_file = os.path.join(
			os.path.join(root_folder, 'data'), filename)
		try:
			with open(user_agents_file) as fp:
				data = [_.strip() for _ in fp.readlines()]
		except:
			data = [default]
		return data
		