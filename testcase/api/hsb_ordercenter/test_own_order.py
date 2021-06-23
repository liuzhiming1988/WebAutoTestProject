#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : test_own_order.py
@Author  : liuzhiming
@Time    : 2021/6/4 9:54
"""

from utils.config_read import ConfigRead
from utils.common import *
from utils.logger import Logger
import allure
import pytest
from apis.own_order import OwnOrder


@allure.feature("【回收宝APP】自有回收订单测试")
class TestOwnOrder:
    # full_name = get_current_project_path() + "\\log\\ownapi_" + get_time()[0:8] + ".log"
    # logger = Logger(full_name).logger

    @allure.story("【回收宝app】回收订单：下单-到店回收")
    @pytest.mark.hsbapitest
    def test_place_order(self, get_token, get_uid):
        OwnOrder().place_order(get_token, get_uid)




if __name__ == '__main__':
    pytest.main(["-v", "-s", "test_own_order.py"])
    # OwnOrderT().place_order()