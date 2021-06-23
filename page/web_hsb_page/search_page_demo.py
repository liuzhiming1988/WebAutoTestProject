# -*- coding: utf-8 -*-
# @Time    : 2021/5/20 23:42
# @Author  : liuzhiming
# @Email   : 
# @File    : search_page_demo.py
# @Software: PyCharm
from base.base_page import BasePage
from selenium.webdriver.common.by import By
import time
from utils.config_read import ConfigRead


class SearchPage(BasePage):
    """百度搜索页面"""
    # 定义元素及操作元素的方法
    url = ConfigRead().get_url("baidu")
    input = ('id', "kw")
    submit = ('id', "su")

    # 元素操作的方法
    def search(self, keywords):

        self.get_url(url=self.url)
        self.send_key(self.input, value=keywords)
        self.click(loc=self.submit)
        time.sleep(3)

