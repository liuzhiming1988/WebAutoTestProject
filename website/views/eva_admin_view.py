#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : eva_admin_view.py
@Author  : liuzhiming
@Time    : 2021/10/21 15:22
"""

from flask import request
from flask import render_template
from flask import Blueprint
from page.eva_admin_page import eva_admin_2C_evaluate, eva_admin_login, eva_admin_menu
from selenium import webdriver
from utils.ding_rebot import DingRebot

eva_blue = Blueprint("eva_admin_view", __name__)


@eva_blue.route("/eva_2c_save", methods=['GET', 'POST'])
def eva_2c_save():
    res_text = ""
    if request.method == "POST":

        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver = webdriver.Chrome(options=options)
        ding_rebot = DingRebot()

        login = eva_admin_login.EvaLoginPage(driver)
        menu = eva_admin_menu.EvaMenuPage(driver)
        eva_2c = eva_admin_2C_evaluate.Eva2cPage(driver)

        login.eva_login()
        menu.enter_2c_evaluate_menu()

        products = request.form.get("products")     # 获取html中提交的参数
        products = products.strip()          # 去除前后空格
        products = products.split(",")
        for product in products:
            res = eva_2c.save_product(product)
            res_text += res + "<br>"

        driver.quit()
        ding_rebot.send_text(res_text)

    return render_template("tips.html", text=res_text)