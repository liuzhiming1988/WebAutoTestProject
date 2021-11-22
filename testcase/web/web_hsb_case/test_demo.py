# -*- coding: utf-8 -*-
# @Time    : 2021/5/20 23:09
# @Author  : liuzhiming
# @Email   : 
# @File    : test_demo.py
# @Software: PyCharm

from page.web_hsb_page.search_page_demo import SearchPage
from utils.logger import LoggerV2
import pytest


class TestSearchBaidu():

    logger = LoggerV2()

    def test_search_01(self, get_driver):
        search = SearchPage(get_driver)
        search.search("回收宝科技")

    @pytest.mark.webtest
    def test_search_02(self, get_driver):
        search = SearchPage(get_driver)
        search.search("回收宝科技2021")


if __name__ == '__main__':
    pytest.main(["-v", "-s", "test_demo.py"])
