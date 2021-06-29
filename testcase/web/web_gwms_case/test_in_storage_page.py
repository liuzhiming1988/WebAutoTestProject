#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : test_in_storage_page.py
@Author  : liuzhiming
@Time    : 2021/6/29 17:09
"""

from utils.common import *
from page.web_gwms_page import login_page
from page.web_gwms_page import menu_page
from page.web_gwms_page import in_storage_orders_page
from utils.logger import Logger
import allure
import pytest


class TestInStorage():
    logger = Logger().logger

    # order = "BB0101210608000003"
    #
    # order = input("请输入商品编码：")

    @pytest.mark.web_gwms
    def test_audit_order(self, get_driver, order):

        login_page_ = login_page.GwmsLoginPage(get_driver)
        menu_page_ = menu_page.GwmsMenuPage(get_driver)
        in_storage_page = in_storage_orders_page.InStoragePage(get_driver)

        login_page_.login()
        menu_page_.open_in_storage_orders()

        in_storage_page.audit_order(order)


if __name__ == '__main__':
    pytest.main(["-v", "-s", "test_in_storage_page.py"])