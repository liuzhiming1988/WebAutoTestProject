#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : eva_admin_login.py
@Author  : liuzhiming
@Time    : 2021/10/20 18:58
"""

from base.base_page import BasePage
from config.config_read import ConfigRead
from utils.common import *
import allure


class EvaLoginPage(BasePage):

    """2.0估价系统后台登录页面"""
    url = "http://evaadmin.huishoubao.com.cn/"
    username = ('xpath', ".//*[@id='username']")
    passwd = ('xpath', ".//*[@id='loginForm']/div[3]/div/div/input")
    submit = ('xpath', ".//*[@id='loginBtn']")

    config = ConfigRead()

    def eva_login(self, username=config.get_account("username"), passwd=config.get_account("passwd")):
        self.get_url(self.url)
        # self.max_window() # mac不兼容
        self.logger.info("开始输入用户名")
        self.send_key(self.username, username)
        self.logger.info("开始输入密码")
        self.send_key(self.passwd, passwd)
        self.logger.info("点击登录")
        self.click(self.submit)
        time.sleep(2)




if __name__ == '__main__':
    from selenium import webdriver

    logger = Logger().logger
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)

    login = EvaLoginPage(driver)
    login.eva_login()
