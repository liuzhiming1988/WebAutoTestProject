#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : test_oms_login.py
@Author  : liuzhiming
@Time    : 2021/5/21 19:27
"""
import unittest
from public.config import ConfigRead
from page_object_hsb.oms_login_page import OmsLoginPage
import time
from public.logger import Logger
from public.common import *
import pytest


class TestOmsLogin(unittest.TestCase):
    """oms系统登录测试"""

    full_name = get_current_project_path() + "\\log\\" + get_time()[0:8] + ".log"
    logger = Logger(full_name).logger
    driver = ConfigRead().get_browser()

    def setUp(self):
        print("开始测试")

    def tearDown(self):
        # self.driver.close()   # 如果还有chrome进程存在，会报错--OSError: [WinError 6] 句柄无效
        self.logger.info("本条用例测试完成，关闭浏览器......")
        self.driver.quit()

    def test_oms_login_01(self):
        """默认账号登录"""
        oms_login = OmsLoginPage(self.driver, self.logger)
        oms_login.oms_login()
        self.logger.info("用例名称：{0}，测试完成".format(get_current_function_name()))

    def test_oms_login_02(self):
        """错误账号登录"""
        oms_login = OmsLoginPage(self.driver, self.logger)
        oms_login.oms_login(username="ghlfd123hg", passwd="36489264783")
        self.logger.info("用例名称：{0}，测试完成".format(get_current_function_name()))


# if __name__ == '__main__':
#     pytest.main()
