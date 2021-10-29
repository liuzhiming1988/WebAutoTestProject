#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : v2_save_spu_2c.py
@Author  : liuzhiming
@Time    : 2021/10/21 11:38
"""

from page.eva_admin_page import eva_admin_2C_evaluate, eva_admin_login, eva_admin_menu
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)

login = eva_admin_login.EvaLoginPage(driver)
menu = eva_admin_menu.EvaMenuPage(driver)
eva_2c = eva_admin_2C_evaluate.Eva2cPage(driver)

login.eva_login()
menu.enter_2c_evaluate_menu()

products = {
    "41567": "iphone X",
    "30831": "iPhone 7",
    "38200": "iPhone 8",
    "3": "iphone 4",
    "23040": "小米4s",
    "23019": "小米 4",
    "63899": "小米 10 Pro（5G）",
    "48187": "荣耀 10",
    "30787": "vivo X9",
    "64177": "三星 Galaxy A71（5G）",
    "30856": "OPPO R7"
}

for product, name in products.items():
    eva_2c.save_product(product)

driver.quit()
