#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : oms_login_page.py
@Author  : liuzhiming
@Time    : 2021/5/21 19:12
"""
from base.base_page import BasePage
from selenium.webdriver.common.by import By
import time
from public.config import ConfigRead


class OmsLoginPage(BasePage):

    """OMS系统后台登录页面"""
    url = ConfigRead().get_url("oms")
    username = (By.XPATH, ".//*[@id='app']/form/div[1]/div/div/input")
    passwd = (By.XPATH, ".//*[@id='app']/form/div[2]/div/div/input")
    submit = (By.XPATH, ".//*[@id='app']/form/div[3]/div/button")

    config = ConfigRead()

    def oms_login(self, username=config.get_account("username"), passwd=config.get_account("passwd")):

        self.get_url(self.url)
        self.send_key(self.username, username)
        self.send_key(self.passwd, passwd)
        self.click(self.submit)

        time.sleep(3)
