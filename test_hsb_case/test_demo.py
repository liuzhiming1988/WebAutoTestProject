# -*- coding: utf-8 -*-
# @Time    : 2021/5/20 23:09
# @Author  : liuzhiming
# @Email   : 
# @File    : test_demo.py
# @Software: PyCharm

import unittest
from public.config import ConfigRead
from page_object_hsb.search_page_demo import SearchPage
from public.common import *
from public.logger import Logger
import pytest


class TestSearchBaidu(unittest.TestCase):

    full_name = get_current_project_path() + "\\log\\" + get_time()[0:8] + ".log"
    logger = Logger(full_name).logger

    def setUp(self):
        self.driver = ConfigRead().get_browser()

    def test_search_01(self):
        search = SearchPage(self.driver, self.logger)
        search.search("回收宝科技")

    def test_search_02(self):
        search = SearchPage(self.driver, self.logger)
        search.search("回收宝科技2021")

    def tearDown(self):
        self.driver.quit()


