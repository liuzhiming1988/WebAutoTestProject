#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : gwms_login_page.py
@Author  : liuzhiming
@Time    : 2021/6/16 11:07
"""


from base.base_page import BasePage
from selenium.webdriver.common.by import By
import time
from public.config import ConfigRead
from public.logger import Logger
from public.common import *
import allure
from page.web_gwms_page import gwsm_conf


class GwmsLoginPage(BasePage):

    """OMS系统后台登录页面"""
    url = gwsm_conf.LOGINURL

    user_name = ("id", "form1:nv_userid")
    password = ("id", "form1:passWord")
    login_button = ("id", "form1:loginBtn")


    def login(self, username="026", password="026"):
        self.get_url(self.url)
        self.max_window()
        self.send_key(self.user_name, username)
        self.send_key(self.password, password)
        self.click(self.login_button)
        time.sleep(5)





