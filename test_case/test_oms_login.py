#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : test_oms_login.py
@Author  : liuzhiming
@Time    : 2021/5/21 19:27
"""
import unittest
from selenium import webdriver
from page_object.oms_login_page import OmsLoginPage


class OmsLogin(unittest.TestCase):
    """oms系统登录测试"""
    def test_oms_login_01(self):
        self.driver = webdriver.Chrome()
        oms_login = OmsLoginPage(self.driver)
        oms_login.oms_login()

    def test_oms_login_02(self):
        self.driver = webdriver.Chrome()
        oms_login = OmsLoginPage(self.driver)
        oms_login.oms_login(username="ghlfd123hg", passwd="36489264783")


if __name__ == '__main__':
    unittest.main()
