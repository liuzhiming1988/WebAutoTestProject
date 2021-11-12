#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : base_price_menu.py
@Author  : liuzhiming
@Time    : 2021/11/10 16:18
"""

from base.base_page import BasePage
from utils.common import *


class BasePriceMenuPage(BasePage):
    """2.0估价系统菜单处理页面"""

    sale_pricing = ('xpath', ".//*[@id='app']/div/div[1]/div[1]/div/ul/div[3]/li/div/span")      # 销售定价父菜单
    sale_price_parameters = ('xpath', "html/body/section/div[2]/div[1]/div/ul/li[4]/ul/li[1]")    # 销售定价-定价参数维护菜单
    sale_price_audit = ('xpath', "html/body/section/div[2]/div[1]/div/ul/li[4]/ul/li[5]")    # 销售定价审核菜单
    price_audit_url = "http://baseprice.huishoubao.com.cn/salePrice/priceAudit"
    spu_list_url = "http://baseprice.huishoubao.com.cn/salePrice/priceParamMaintain/spuList"
    recycle_pricing_param_url = "http://baseprice.huishoubao.com.cn/recyclePricing/spuList"
    recycle_pricing_audit_url = "http://baseprice.huishoubao.com.cn/recyclePricing/audit"

    def enter_sale_parameters_menu(self):
        """进入销售定价参数维护菜单"""
        self.get_url(self.spu_list_url)
        self.max_window()
        time.sleep(2)

    def enter_sale_audit_menu(self):
        """进入销售定价审核菜单"""
        self.get_url(self.price_audit_url)
        self.max_window()
        time.sleep(2)

    def enter_recycle_pricing_param_menu(self):
        """进入回收定价参数维护菜单"""
        self.get_url(self.recycle_pricing_param_url)
        self.max_window()
        time.sleep(2)

    def enter_recycle_pricing_audit_menu(self):
        """进入回收定价审核菜单"""
        self.get_url(self.recycle_pricing_audit_url)
        self.max_window()
        time.sleep(2)


if __name__ == '__main__':
    from selenium import webdriver

    logger = Logger().logger
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)

    login = BasePriceMenuPage(driver)
    login.enter_sale_parameters_menu()