#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : test_get_balance.py
@Author  : liuzhiming
@Time    : 2021/6/4 11:48
"""

from utils.config_read import ConfigRead
from utils.common import *
from utils.logger import Logger
import allure
import pytest
from apis.get_balance import GetBalanceInfo

@allure.feature("【回收宝APP】账户信息测试")
class TestGetBalance:
    # full_name = get_current_project_path() + "\\log\\" + get_time()[0:8] + ".log"
    # logger = Logger(full_name).logger
    @allure.story("【回收宝APP】账户：获取个人钱包信息")
    @pytest.mark.hsbapitest
    def test_get_balance_info(self, get_token, get_uid):
        GetBalanceInfo().get_balance_info(get_token, get_uid)


if __name__ == '__main__':
    pytest.main(["-v", "-s", "test_get_balance.py"])
    # TestGetBalance().test_get_balance_info()