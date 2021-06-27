#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : test_oms_login.py
@Author  : liuzhiming
@Time    : 2021/5/21 19:27
"""
from page.web_hsb_page.oms_login_page import OmsLoginPage
from utils.common import *
import allure
import pytest


# @allure.feature("OMS系统:登录功能")
class TestOmsLogin:
    """oms系统登录测试"""

    logger = Logger().logger

    login_test_data = [
        ({"username":"fdafdaf", "password":""}, "fail", "不输入密码"),
        ({"username":"fdfag", "password":"fdagdaf"}, "fail", "错误的用户名和密码"),
        ({"username":"test_liuzhiming@huishoubao.com.cn", "password":"32rfdfs"}, "fail", "错误的密码"),
        ({"username":"test_liuzhiming@huishoubao.com.cn", "password":"f6758a4e"}, "success", "正确的用户名和密码"),
        ({"username":"", "password":""}, "block", "用户名和密码为空")
    ]

    @allure.story("订单系统-登录用例")
    @allure.title("{case_name}")
    @pytest.mark.webtest
    @pytest.mark.parametrize("login_data, expect, case_name",login_test_data)
    def test_oms_login(self, get_driver, login_data, expect, case_name):
        # allure中，用例的描述部分
        """订单系统-Web-UI自动化：登录测试用例{}""".format(case_name)
        oms_login = OmsLoginPage(get_driver)
        oms_login.oms_login(login_data["username"], login_data["password"])
        self.logger.info("用例名称：{0}，测试完成".format(get_current_function_name()))


if __name__ == '__main__':
    pytest.main(["-v", "-s", "test_oms_login.py"])
