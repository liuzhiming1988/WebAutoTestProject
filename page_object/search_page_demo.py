# -*- coding: utf-8 -*-
# @Time    : 2021/5/20 23:42
# @Author  : liuzhiming
# @Email   : 
# @File    : search_page_demo.py
# @Software: PyCharm
from base.base_page import BasePage

class SearchPage(BasePage):
    """百度搜索页面"""
    # 定义元素及操作元素的方法
    url = "https://www.baidu.com"
    input = (By.ID,"kw")
    submit = (By.ID,"su")

    # 元素操作的方法
    def search(self,keywords):

        self.getUrl(url=self.url)
        self.send_key(loc=self.input,value=keywords)
        self.click(loc=self.submit)
        time.sleep(3)

