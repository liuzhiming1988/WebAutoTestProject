#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : test_gwms_login.py
@Author  : liuzhiming
@Time    : 2021/6/16 11:06
"""

from utils.config_read import ConfigRead
from page.web_gwms_page.gwms_login_page import GwmsLoginPage
from utils.common import *
from utils.logger import Logger
import allure
import pytest


class TestLogin:
    full_name = get_current_project_path() + "\\log\\" + get_time()[0:8] + ".log"
    logger = Logger(full_name).logger

    @pytest.mark.webtest
    def test_login_01(self, get_driver):

        gwms = GwmsLoginPage(get_driver, self.logger)
        gwms.login("026", "026")


if __name__ == '__main__':
    pytest.main(["-v", "-s", "test_gwms_login.py"])