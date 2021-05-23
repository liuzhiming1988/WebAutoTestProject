#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : test_oms_login.py
@Author  : liuzhiming
@Time    : 2021/5/21 19:27
"""
import unittest
from selenium import webdriver
from public.config import ConfigRead
from page_object.oms_login_page import OmsLoginPage
import common


class OmsLogin(unittest.TestCase):
    """oms系统登录测试"""
    def setUp(self):
        self.driver = ConfigRead().get_browser()

    def test_oms_login_01(self):
        """默认账号登录"""
        oms_login = OmsLoginPage(self.driver)
        oms_login.oms_login()

    def test_oms_login_02(self):
        """错误账号登录"""
        oms_login = OmsLoginPage(self.driver)
        oms_login.oms_login(username="ghlfd123hg", passwd="36489264783")

    def tearDown(self):

        # self.driver.close()   # 如果还有chrome进程存在，会报错--OSError: [WinError 6] 句柄无效
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
