# -*- coding: utf-8 -*-
# @Time    : 2021/5/20 23:09
# @Author  : liuzhiming
# @Email   : 
# @File    : test_demo.py
# @Software: PyCharm

from public.config_read import ConfigRead
from page.web_hsb_page.search_page_demo import SearchPage
from public.common import *
from public.logger import Logger
import pytest


class TestSearchBaidu():

    full_name = get_current_project_path() + "\\log\\" + get_time()[0:8] + ".log"
    logger = Logger(full_name).logger

    def test_search_01(self, get_driver):
        search = SearchPage(get_driver, self.logger)
        search.search("回收宝科技")

    @pytest.mark.webtest
    def test_search_02(self, get_driver):
        search = SearchPage(get_driver, self.logger)
        search.search("回收宝科技2021")


if __name__ == '__main__':
    pytest.main(["-v", "-s", "test_demo.py"])
