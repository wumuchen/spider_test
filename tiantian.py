import requests
from lxml import etree
import json

# # 测试
# headers = {
# 	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
# }
# url = "http://fund.eastmoney.com/api/Dtshph.ashx?t=0&c=yndt&s=desc&issale=&page=1&psize=200&callback=jQuery18301398017601166126_1531738183728&_=1531738184291"
# response = requests.get(url, headers=headers)
# print(response.url)
# print(response.content.decode())

class TiantianSpider:
	def __init__(self):
		self.temp_url = "http://fund.eastmoney.com/api/Dtshph.ashx?t=0&c=yndt&s=desc&issale=&page=%d&psize=200&callback=jQuery18301398017601166126_1531738183728&_=1531738184291"
		self.prefix = "http://fund.eastmoney.com"
		self.headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
		}

	def parse_url(self, url):
		print(url)
		return requests.get(url, headers=self.headers).content.decode()

	def get_content_list(self, html_str):
		item_list = []

		# print(html_str)
		# print(html_str[41:-1])
		json_data = json.loads(html_str[41:-1])

		html = etree.HTML(json_data["data"])
		tr_list = html.xpath('//tr')
		for tr in tr_list:
			item = {}
			item["number"] = tr.xpath('./td[3]/a/text()')[0]
			item["url"] = self.prefix+tr.xpath('./td[3]/a/@href')[0]
			item["name"] = tr.xpath('./td[4]/a/text()')[0]
			item["links"] = []
			for link in tr.xpath('./td[5]/a'):
				a = {}
				a["text"] = link.xpath("./text()")[0]
				a["url"] = self.prefix+link.xpath("./@href")[0]
				item["links"].append(a)
			item["dyjz"] = tr.xpath('./td[6]/span/text()')[0]
			item["date"] = tr.xpath('./td[7]/text()')[0]
			item["1year"] = "".join(tr.xpath('./td[8]//text()')).strip()
			item["2year"] = "".join(tr.xpath('./td[9]//text()')).strip()
			item["3year"] = "".join(tr.xpath('./td[10]//text()')).strip()
			item["5year"] = "".join(tr.xpath('./td[11]//text()')).strip()
			item["pingji"] = tr.xpath('./td[12]/span/text()')[0]
			item["feilv"] = tr.xpath('./td[13]//a/text()')[0]
			print(item)
			item_list.append(item)

		return item_list, json_data["total"]

	def save_content_list(self, item_list):
		pass

	def run(self):
		page = 1
		pagesize = 200
		total = 1
		while (page - 1) * pagesize < total:
			url = self.temp_url % page
			html_str = self.parse_url(url)
			item_list, total = self.get_content_list(html_str)
			self.save_content_list(item_list)
			page += 1

		print("完成")

if __name__ == '__main__':
	spider = TiantianSpider()
	spider.run()


