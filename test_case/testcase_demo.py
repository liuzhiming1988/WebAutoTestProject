# -*- coding: utf-8 -*-
# @Time    : 2021/5/20 23:09
# @Author  : liuzhiming
# @Email   : 
# @File    : testcase_demo.py
# @Software: PyCharm

import unittest
from selenium import webdriver
from page_object.search_page_demo import SearchPage

class SearchBaidu(unittest.TestCase):

    # def __int__(self):
    #     self.driver = webdriver.Chrome()

    def test_search_01(self):
        self.driver = webdriver.Chrome()
        search = SearchPage(self.driver)
        search.search("回收宝科技")

    def test_search_02(self):
        self.driver = webdriver.Chrome()
        search = SearchPage(self.driver)
        search.search("回收宝科技2021")



if __name__ == '__main__':
    unittest.main()
