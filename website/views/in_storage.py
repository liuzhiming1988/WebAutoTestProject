#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : in_storage.py
@Author  : liuzhiming
@Time    : 2021/7/1 16:14
"""

from page.web_gwms_page import login_page
from page.web_gwms_page import menu_page
from page.web_gwms_page import in_storage_orders_page
from page.web_gwms_page import shipper_allocation_page
from utils.logger import Logger
from selenium import webdriver


class TestInStorage:

    def test_add_storage_order(self, barCode):
        """
        添加入库单：
        1.入库处理
        2.入库单
        """
        text = ""    # 接收执行结果
        logger = Logger().logger
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        get_driver = webdriver.Chrome(options=options)

        login_page_ = login_page.GwmsLoginPage(get_driver)
        menu_page_ = menu_page.GwmsMenuPage(get_driver)
        in_storage_page = in_storage_orders_page.InStoragePage(get_driver)
        shipper_allocation_page_ = shipper_allocation_page.ShipperAllocationPage(get_driver)

        login_page_.login()

        # 入库处理：获取来源单号
        menu_page_.open_in_storage_orders()
        source_order = in_storage_page.audit_order(barCode)
        logger.debug("【{}】对应的来源单号为：【{}】".format(barCode, source_order))

        # source_order = "A2106301833432E12"

        # 判断来源单号是否获取到，获取到则进行入库操作
        if source_order:

            text = "1. 入库处理：单据审核成功，来源单号为：{}<br>".format(source_order)

            # 添加货主物料配置
            menu_page_.open_shipper_material_allocation()
            shipper_allocation_page_.add_material_code()
            text += "2. 添加货主物料配置成功；<br>"

            # 入库单添加与审核
            menu_page_.open_storage_order()
            text += in_storage_page.add_storage_order(source_order)
        else:
            text = "1. 没有来源单号，无法入库，请检查，商品编码【{}】".format(barCode)
            logger.error(text)

        get_driver.quit()
        return text


if __name__ == '__main__':

    # test = TestInStorage()
    # barCode = "TY32674628353242343"
    # test.test_add_storage_order(barCode)
    print(len("ZY0101210630000038"))
