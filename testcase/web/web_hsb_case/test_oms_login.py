#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : test_oms_login.py
@Author  : liuzhiming
@Time    : 2021/5/21 19:27
"""
import unittest
from public.config_read import ConfigRead
from page.web_hsb_page.oms_login_page import OmsLoginPage
from public.logger import Logger
from public.common import *
import allure
import pytest


@allure.feature("OMS系统:登录功能")
class TestOmsLogin:
    """oms系统登录测试"""

    logger = Logger().logger

    @allure.story("正确用户名、密码，成功登录")
    @pytest.mark.webtest
    def test_oms_login_01(self, get_driver):
        """默认账号登录"""
        oms_login = OmsLoginPage(get_driver)
        oms_login.oms_login()
        self.logger.info("用例名称：{0}，测试完成".format(get_current_function_name()))

    @allure.story("错误的账号和密码，登录失败")
    def test_oms_login_02(self, get_driver):
        """错误账号登录"""
        oms_login = OmsLoginPage(get_driver)
        oms_login.oms_login(username="ghlfd123hg", passwd="36489264783")
        self.logger.info("用例名称：{0}，测试完成".format(get_current_function_name()))


if __name__ == '__main__':
    pytest.main(["-v", "-s", "test_oms_login.py"])
