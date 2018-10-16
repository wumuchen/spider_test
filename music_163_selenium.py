from selenium import webdriver
import time

sleep_time = 5

class NeteaseMuiscSpider:
	def __init__(self):
		# 网址
		self.start_url = "http://music.163.com/"
		# 创建一个chrome浏览器
		self.driver = webdriver.Chrome()

	def get_content_list(self):
		# 歌单列表
		item_list = []

		# 切换框架
		self.driver.switch_to.frame("g_iframe")

		# 获取有所的列表
		li_list = self.driver.find_elements_by_xpath('//ul[@id="m-pl-container"]/li')

		# 根据元素数量进行循环
		for i in range(1, len(li_list)+1):
			# 获取对应位置的li元素
			li = self.driver.find_element_by_xpath('//ul[@id="m-pl-container"]/li[%d]' % i)

			# 点击超链接进入到歌单内容
			li.find_element_by_xpath('.//a').click()

			# 等待5秒
			time.sleep(sleep_time)

			# 获取歌单内容
			item = {}
			# 名称
			item["name"] = self.driver.find_element_by_xpath('.//h2').text
			# 歌曲列表
			item["list"] = []
			# 获取所有的tr标签
			tr_list = self.driver.find_elements_by_xpath('.//table[contains(@class, "m-table")]/tbody/tr')
			# 循环获取内容
			for tr in tr_list:
				# 音乐数据
				music = {}
				# 编号
				music["num"] = tr.find_element_by_xpath('./td[1]//span[@class="num"]').text
				# 歌名
				music["title"] = tr.find_element_by_xpath('./td[2]//b[@title]').get_attribute("title").replace("\xa0", " ")
				# 打印数据
				print(music)
				# 将歌曲添加到歌单中
				item["list"].append(music)
			# 打印歌单
			print(item)
			# 将歌单添加到歌单列表
			item_list.append(item)

			# 浏览器后退
			self.driver.back()
			# 切换框架
			self.driver.switch_to.frame("g_iframe")

		# 获取下一页
		next_url = self.driver.find_elements_by_xpath('.//a[@class="zbtn znxt"]')
		next_url = next_url[0] if len(next_url) > 0 else None

		# 返回歌单列表和下一页
		return item_list, next_url

	def save_content_list(self, item_list):
		pass

	def run(self):
		# 打开网易云音乐
		self.driver.get(self.start_url)

		# 获取歌单链接 并单击
		self.driver.find_element_by_xpath('//em[text()="歌单"]/..').click()
		# 点击之后浏览器地址没有更改 可以判断为js事件 所以等待几秒
		time.sleep(sleep_time)

		# 获取内容
		item_list, next_url = self.get_content_list()

		# 保存歌单
		self.save_content_list(item_list)

		# 获取下一页的内容
		while next_url is not None:
			# 获取内容
			item_list, next_url = self.get_content_list()

			# 保存歌单
			self.save_content_list(item_list)

		print("完成")

		# 退出
		self.driver.quit()


if __name__ == '__main__':
	spider = NeteaseMuiscSpider()
	spider.run()
