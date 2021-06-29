#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : login_page.py
@Author  : liuzhiming
@Time    : 2021/6/16 11:07
"""


from base.base_page import BasePage
from utils.common import *
from page.web_gwms_page import conf


class GwmsLoginPage(BasePage):

    """OMS系统后台登录页面"""
    URL = conf.LOGINURL
    UNAME = conf.USERNAME
    PWD = conf.PASSWORD

    user_name = ("id", "form1:nv_userid")
    password = ("id", "form1:passWord")
    login_button = ("id", "form1:loginBtn")

    def goto_loginpage(self, url):
        self.get_url(url)

    def set_username(self, username):
        self.send_key(self.user_name, username)

    def set_password(self, password):
        self.send_key(self.password, password)

    def click_loginButton(self):
        self.click(self.login_button)

    def wait_login(self, timeout=5):
        if isinstance(timeout, int):
            time.sleep(timeout)
        else:
            self.logger.info("等待时间必须是int类型")

    def login(self, username=None, password=None):
        # 如果没传用户名和密码，就用配置文件中的默认值
        if username is None:
            username = self.UNAME
            password = self.PWD
        self.goto_loginpage(self.URL)
        self.set_username(username)
        self.set_password(password)
        self.click_loginButton()
        self.wait_login()



