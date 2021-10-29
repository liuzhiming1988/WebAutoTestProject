#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : eva_admin_menu.py
@Author  : liuzhiming
@Time    : 2021/10/20 18:58
"""

from base.base_page import BasePage
from config.config_read import ConfigRead
from utils.common import *
import allure


class EvaMenuPage(BasePage):
    """2.0估价系统菜单处理页面"""
    open_menu = ("xpath", ".//*[@id='app']/div/div[2]/div[1]/div[1]")     # 展开左侧菜单栏
    product_library = ('xpath', ".//*[@id='app']/div/div[1]/div[1]/div/ul/div[3]/li/div/span")      # 新产品库父菜单
    eva_2C = ('xpath', ".//*[@id='app']/div/div[1]/div[1]/div/ul/div[3]/li/ul/a[4]/li/span")    # 2C估价菜单
    submit = ('xpath', ".//*[@id='loginBtn']")

    def enter_2c_evaluate_menu(self):

        self.click(self.open_menu)
        # self.click(self.product_library)
        # self.click(self.eva_2C)
        self.get_url("http://evaadmin.huishoubao.com.cn/toC/index")
        self.max_window()
        time.sleep(2)


if __name__ == '__main__':
    from selenium import webdriver

    logger = Logger().logger
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)

    login = EvaMenuPage(driver)
    login.enter_2c_evaluate_menu()
