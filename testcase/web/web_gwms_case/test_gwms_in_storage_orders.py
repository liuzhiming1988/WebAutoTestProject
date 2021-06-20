#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : test_gwms_in_storage_orders.py
@Author  : liuzhiming
@Time    : 2021/6/16 16:59
"""

from public.config_read import ConfigRead
from page.web_gwms_page.gwms_menu_page import GwmsMenu
from page.web_gwms_page.gwms_login_page import GwmsLoginPage
from public.common import *
from public.logger import Logger
import allure
import pytest


class TestInStorageOrders:
    full_name = get_current_project_path() + "\\log\\" + get_time()[0:8] + ".log"
    logger = Logger(full_name).logger

    @pytest.mark.web_gwms
    def test_add_bill(self,get_driver):
        GwmsLoginPage(get_driver, self.logger).login()
        GwmsMenu(get_driver, self.logger).open_in_storage_orders()
        time.sleep(10)



if __name__ == '__main__':
    pytest.main(["-v", "-s", "test_gwms_in_storage_orders.py"])