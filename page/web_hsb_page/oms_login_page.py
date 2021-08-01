#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : oms_login_page.py
@Author  : liuzhiming
@Time    : 2021/5/21 19:12
"""
from base.base_page import BasePage
from config.config_read import ConfigRead
from utils.common import *
import allure


class OmsLoginPage(BasePage):

    """OMS系统后台登录页面"""
    url = ConfigRead().get_value("url", "oms")
    username = ('xpath', ".//*[@id='views']/form/div[1]/div/div/input")
    passwd = ('xpath', ".//*[@id='views']/form/div[2]/div/div/input")
    submit = ('xpath', ".//*[@id='views']/form/div[3]/div/button")

    config = ConfigRead()

    def oms_login(self, username=config.get_account("username"), passwd=config.get_account("passwd")):
        self.get_url(self.url)
        # self.max_window() # mac不兼容
        self.logger.info("开始输入用户名")
        with allure.step("开始输入用户名"):
            self.send_key(self.username, username)
            allure.attach("输入完成{0}".format(username))
        self.logger.info("开始输入密码")
        self.send_key(self.passwd, passwd)
        self.logger.info("点击登录")
        self.click(self.submit)
        time.sleep(2)


