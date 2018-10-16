import requests
import json
import base64
import re
from lxml import etree

class BilibiliSpider:
	def __init__(self):
		self.list_url = "https://api.bilibili.com/x/web-interface/newlist?rid=171&type=0&pn=%d&ps=20"
		self.video_url = "https://www.bilibili.com/video/av%d/"
		# self.comment_url = "https://comment.bilibili.com/%d.xml"
		self.comment_url = "https://api.bilibili.com/x/v1/dm/list.so?oid=%d"
		self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",}

	def get_url_list(self):
		return [self.list_url % i for i in range(1,3)]

	def parse_url(self, url):
		html = requests.get(url, headers=self.headers).content.decode("utf-8")
		file_tmpl = "bilibili/page_%s.html"
		file_index = file_tmpl % "index"
		file_name = file_tmpl % base64.urlsafe_b64encode(url.encode("utf-8")).decode("utf-8")
		with open(file_index, "a", encoding="utf-8") as f:
			f.write('<a href="../%s">%s</a><br>\n' % (file_name, url))
		with open(file_name, "w", encoding="utf-8") as f:
			f.write(html)
		return html

	def get_content_list(self, html):
		return json.loads(html)["data"]["archives"]

	def save_content_list(self, content_list):
		with open("bilibili/list.txt", "a", encoding="utf-8") as f:
			for content in content_list:
				f.write(json.dumps(content, ensure_ascii=False, indent=4))
				f.write("\n")

	def get_video_info(self, html):
		json_str = re.findall(r"<script>window\.__INITIAL_STATE__=(.*?);\(function\(\)\{var s;", html)[0]
		return json.loads(json_str)

	def save_video_info(self, video):
		with open("bilibili/video_%s.txt" % video["aid"], "w", encoding="utf-8") as f:
			f.write(json.dumps(video, ensure_ascii=False, indent=4))

	def get_comment_list(self, html):
		comment_list = []
		elem = etree.HTML(html.encode("utf-8"))
		ds = elem.xpath("//d")
		for d in ds:
			comment = {}
			comment["content"] = d.xpath("text()")[0]
			comment["p"] = d.xpath("@p")[0]
			comment_list.append(comment)
		return comment_list

	def save_comment_list(self, comment_list, aid):
		with open("bilibili/comment_%s.txt" % aid, "a", encoding="utf-8") as f:
			for comment in comment_list:
				f.write(json.dumps(comment, ensure_ascii=False, indent=2))
				f.write("\n")

	def run(self):
		# 构建url
		url_list = self.get_url_list()

		for url in url_list:
			# 获取视频页面html
			list_html = self.parse_url(url)
			print(list_html)
			# 分析视频页面
			content_list = self.get_content_list(list_html)
			# 设置视频页面
			self.save_content_list(content_list)

			# 测试所以每页只获取了两个
			content_list = content_list[18:20]
			for content in content_list:
				# 获取视频页面html
				video_html = self.parse_url(self.video_url % content["aid"])
				# 分析视频页面
				video_info = self.get_video_info(video_html)
				# 设置视频页面
				self.save_video_info(video_info)

				# 获取弹幕内容
				comment_html = self.parse_url(self.comment_url % video_info["videoData"]["pages"][0]["cid"])
				# 分析弹幕内容
				comment_list = self.get_comment_list(comment_html)
				# 设置弹幕内容
				self.save_comment_list(comment_list, video_info["aid"])

if __name__ == '__main__':
	spider = BilibiliSpider()
	spider.run()
