import requests
from lxml import etree
from pymongo import MongoClient


class NeteaseSpider:
	def __init__(self):
		self.start_url = "http://music.163.com/discover/playlist"
		self.prefix_url = "http://music.163.com"
		self.headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
			"Referer": "http://music.163.com/",
		}
		self.client = MongoClient()
		self.collection = self.client.test.music

	def __del__(self):
		self.client.close()

	def parse_url(self, url):
		print(url)
		return requests.get(url, headers=self.headers).content.decode()

	def get_playlist_list(self, url):
		item_list = []

		html_str = self.parse_url(url)
		# with open('music/1.html', 'w', encoding='utf-8')as f:
		# 	f.write(html_str)
		# with open('music/1.html', 'r', encoding='utf-8')as f:
		# 	html_str = f.read()
		html = etree.HTML(html_str)

		li_list = html.xpath('//ul[@id="m-pl-container"]/li')
		for li in li_list:
			item = {}
			item["title"] = li.xpath('.//a/@title')[0]
			item["author"] = li.xpath('.//a/@title')[-1]
			item["num"] = li.xpath('.//span[@class="nb"]/text()')[0]
			item["music_list"] = self.get_play_list(self.prefix_url + li.xpath('.//a/@href')[0], item)
			# item["music_list"] = self.prefix_url+li.xpath('.//a/@href')[0]
			item_list.append(item)

		next_url = html.xpath('.//a[@class="zbtn znxt"]/@href')
		next_url = self.prefix_url + next_url[0] if len(next_url) > 0 else None

		return item_list, next_url

	def save_playlist_list(self, playlist_list):
		pass

	def get_play_list(self, url, item):
		item_list = []

		html_str = self.parse_url(url)
		# with open('music/%s.html' % item['title'], 'w', encoding='utf-8')as f:
		# 	f.write(html_str)
		# with open('music/%s.html' % item['title'], 'r', encoding='utf-8')as f:
		# 	html_str = f.read()
		html = etree.HTML(html_str)

		item["title_num"] = html.xpath('.//span[@id="playlist-track-count"]/text()')[0]
		item["play_time"] = html.xpath('.//strong[@id="play-count"]/text()')[0]

		tr_list = html.xpath('.//ul[@class="f-hide"]/li')
		for tr in tr_list:
			item = {}
			item["name"] = tr.xpath('./a/text()')[0]
			# item["time"] = tr.xpath('./a/text()')[0]
			item["href"] = self.prefix_url + tr.xpath('./a/@href')[0]
			# print(item)
			item_list.append(item)

		return item_list

	def save_play_list(self, playlist_list):
		self.collection.insert(playlist_list)

	def run(self):
		next_url = self.start_url
		while next_url is not None:
			playlist_list, next_url = self.get_playlist_list(next_url)
			self.save_play_list(playlist_list)
			print('ok')
			if 1 == 1:
				break


if __name__ == '__main__':
	spider = NeteaseSpider()
	spider.run()
