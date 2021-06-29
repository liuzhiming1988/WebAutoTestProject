#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : test_shipper_allocation.py
@Author  : liuzhiming
@Time    : 2021/6/28 18:28
"""

from page.web_gwms_page import login_page
from page.web_gwms_page import menu_page
from page.web_gwms_page import shipper_allocation_page
from utils.common import *
from utils.logger import Logger
import allure
import pytest


class TestShipperAllocation:

    logger = Logger().logger

    @pytest.mark.web_gwms
    def test_add_material_code(self, get_driver):

        login_page_ = login_page.GwmsLoginPage(get_driver)
        menu_page_ = menu_page.GwmsMenuPage(get_driver)
        shipper_allocation_page_ = shipper_allocation_page.ShipperAllocationPage(get_driver)

        login_page_.login()
        menu_page_.open_shipper_material_allocation()

        shipper_allocation_page_.add_material_code()




if __name__ == '__main__':
    pytest.main(["-v", "-s", "test_shipper_allocation.py"])