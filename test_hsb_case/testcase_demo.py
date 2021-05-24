# -*- coding: utf-8 -*-
# @Time    : 2021/5/20 23:09
# @Author  : liuzhiming
# @Email   : 
# @File    : testcase_demo.py
# @Software: PyCharm

import unittest
from public.config import ConfigRead
from page_object_hsb.search_page_demo import SearchPage


class SearchBaidu(unittest.TestCase):

    def setUp(self):
        self.driver = ConfigRead().get_browser()

    def test_search_01(self):
        search = SearchPage(self.driver)
        search.search("回收宝科技")

    def test_search_02(self):
        search = SearchPage(self.driver)
        search.search("回收宝科技2021")

    def tearDown(self) -> None:
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
