#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : test_in_storage.py
@Author  : liuzhiming
@Time    : 2021/6/29 17:09
"""

from utils.common import *
from page.web_gwms_page import login_page
from page.web_gwms_page import menu_page
from page.web_gwms_page import in_storage_orders_page
from page.web_gwms_page import shipper_allocation_page
from utils.logger import Logger
import allure
import pytest


class TestInStorage():
    logger = Logger().logger

    # barCode = ["ZY0101210630000039", "ZY0101210630000038", "ZY0101210630000037"]

    @pytest.mark.web_gwms
    # @pytest.mark.parametrize("barCode", barCode)
    def test_add_storage_order(self, get_driver, barCode):
        """
        添加入库单：
        1.入库处理
        2.入库单
        """
        login_page_ = login_page.GwmsLoginPage(get_driver)
        menu_page_ = menu_page.GwmsMenuPage(get_driver)
        in_storage_page = in_storage_orders_page.InStoragePage(get_driver)
        shipper_allocation_page_ = shipper_allocation_page.ShipperAllocationPage(get_driver)

        login_page_.login()

        # 添加货主物料配置
        menu_page_.open_shipper_material_allocation()
        shipper_allocation_page_.add_material_code()

        # 入库处理：获取来源单号
        menu_page_.open_in_storage_orders()
        source_order = in_storage_page.audit_order(barCode)
        self.logger.debug("【{}】对应的来源单号为：【{}】".format(barCode,source_order))

        # source_order = "A2106301833432E12"

        #判断来源单号是否获取到，获取到则进行入库操作
        if source_order is not False:
            menu_page_.open_storage_order()
            in_storage_page.add_storage_order(source_order)
        else:
            self.logger.error("没有来源单号，无法入库，请检查，商品编码【{}】".format(barCode))

        # test定位元素
        # menu_page_.open_storage_order()
        # in_storage_page.test_button()

if __name__ == '__main__':
    pytest.main(["-v", "-s", "test_in_storage.py"])