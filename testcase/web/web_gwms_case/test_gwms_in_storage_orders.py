#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : test_gwms_in_storage_orders.py
@Author  : liuzhiming
@Time    : 2021/6/16 16:59
"""

from page.web_gwms_page.gwms_menu_page import GwmsMenu
from page.web_gwms_page.gwms_login_page import GwmsLoginPage
from utils.common import *
from utils.logger import Logger
import pytest


class TestInStorageOrders:

    @pytest.mark.web_gwms
    def test_add_bill(self, get_driver):
        GwmsLoginPage(get_driver).login()
        GwmsMenu(get_driver).open_in_storage_orders()
        time.sleep(10)



if __name__ == '__main__':
    pytest.main(["-v", "-s", "test_gwms_in_storage_orders.py"])