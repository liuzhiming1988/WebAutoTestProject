#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : test_gwms_login.py
@Author  : liuzhiming
@Time    : 2021/6/16 11:06
"""

from page.web_gwms_page.login_page import GwmsLoginPage
from utils.logger import LoggerV2
import allure
import pytest


class TestLogin:

    logger = LoggerV2()

    login_test_data = [
        ({"username": "test_liuzhiming@huishoubao.com.cn", "password": "32rfdfs"}, "fail", "登录：错误的密码"),
        ({"username": "030", "password": "030"}, "success", "正确的用户名和密码"),
        ({"username": "030", "password": ""}, "success", "密码为空"),
        ({"username": "", "password": ""}, "block", "错误：用户名和密码为空")
    ]

    @allure.story("巨沃系统-登录测试用例")
    @allure.title("{case_name}")
    @pytest.mark.demo
    @pytest.mark.parametrize("login_data, expect, case_name", login_test_data )
    def test_login_01(self, get_driver, login_data, expect, case_name):

        gwms = GwmsLoginPage(get_driver)
        gwms.login(login_data["username"], login_data["password"])


if __name__ == '__main__':
    pytest.main(["-v", "-s", "test_gwms_login.py"])