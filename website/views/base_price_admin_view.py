#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : base_price_admin_view.py
@Author  : liuzhiming
@Time    : 2021/11/11 9:51
"""

from flask import request
from flask import render_template
from flask import Blueprint
from page.base_price_page import base_price_login, base_price_menu, base_price_sale_parameters, base_price_sale_audit
from page.base_price_page import recycle_pricing_audit, recycle_pricing_param
from selenium import webdriver
from utils.ding_rebot import DingRebot

base_price_blue = Blueprint("base_price_admin_view", __name__)


@base_price_blue.route("/save_sale_price_v3", methods=['GET', 'POST'])
def save_sale_price_v3():
    res_text = "【价格3.0-保存并审核销售定价参数】<br>"
    if request.method == "POST":
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver = webdriver.Chrome(options=options)
        ding_rebot = DingRebot()

        login = base_price_login.BasePriceLoginPage(driver)
        menu = base_price_menu.BasePriceMenuPage(driver)
        price_param_maintain = base_price_sale_parameters.PriceParamMaintainPage(driver)
        price_audit = base_price_sale_audit.PriceAuditPage(driver)

        login.base_price_login()

        sale_product_ids = request.form.get("sale_product_ids")  # 获取html中提交的参数
        sale_product_ids = sale_product_ids.strip()  # 去除前后空格
        sale_product_ids = sale_product_ids.split(",")

        for product in sale_product_ids:
            try:
                menu.enter_sale_parameters_menu()
                if price_param_maintain.submit_audit(product):
                    menu.enter_sale_audit_menu()
                    res_text += price_audit.pass_audit(product) + "<br>"
                else:
                    res_text += "机型【{}】未找到 提交审核 按钮，请检查！".format(product)
            except Exception as ec:
                res_text += "机型【{}】审核失败：【{}】".format(product, repr(ec)) + "<br>"
                login.logger.error(res_text)
        driver.quit()
    return render_template("tips.html", text=res_text)


@base_price_blue.route("/save_recycle_price_v3", methods=['GET', 'POST'])
def save_recycle_price_v3():
    res_text = "【价格3.0-保存并审核回收定价参数】<br>"
    if request.method == "POST":
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver = webdriver.Chrome(options=options)
        ding_rebot = DingRebot()

        login = base_price_login.BasePriceLoginPage(driver)
        menu = base_price_menu.BasePriceMenuPage(driver)
        recycle_pricing = recycle_pricing_param.RecyclePriceParamPage(driver)
        rp_audit = recycle_pricing_audit.RecyclePricingAuditPage(driver)

        login.base_price_login()

        recycle_product_ids = request.form.get("recycle_product_ids")   # 获取html中提交的参数
        recycle_product_ids = recycle_product_ids.strip()   # 去除前后空格
        recycle_product_ids = recycle_product_ids.split(",")

        for product in recycle_product_ids:
            try:
                menu.enter_recycle_pricing_param_menu()
                if recycle_pricing.submit_audit(product):
                    menu.enter_recycle_pricing_audit_menu()
                    res_text += rp_audit.pass_audit(product) + "<br>"
                else:
                    res_text += "机型【{}】未找到可操作的记录，请检查！".format(product)
            except Exception as ec:
                res_text += "机型【{}】审核失败：【{}】".format(product, repr(ec)) + "<br>"
                login.logger.error(res_text)
        driver.quit()
    return render_template("tips.html", text=res_text)

