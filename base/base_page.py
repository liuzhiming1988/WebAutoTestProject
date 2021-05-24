# -*- coding: utf-8 -*-
# @Time    : 2021/5/20 23:10
# @Author  : liuzhiming
# @Email   : 
# @File    : base_page.py
# @Software: PyCharm
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from public.logger import Logger
import os
import time
import sys
from public.common import *


class BasePage:
    # 封装每个页面共同的属性和方法

    def __init__(self, driver ,logger):
        self.driver = driver
        self.logger = logger

    # 定位属性方法
    def loctor(self, loc):
        """
        元素定位

        :arg:
         - loc - 传入一个元组，如input = (By.ID, "kw")
        :return:
         - 返回元素对象
        """
        self.logger.info("开始寻找元素{0}".format(loc))
        WebDriverWait(self.driver, 15, 0.5).until(EC.visibility_of_element_located(loc))
        self.logger.info("已找到元素{0}".format(loc))
        return self.driver.find_element(*loc)

    def send_key(self, loc, value):
        """输入方法"""
        self.loctor(loc).send_keys(value)
        self.logger.warning("元素{0},输入{1}".format(loc, value))

    def click(self, loc):
        """点击"""
        self.loctor(loc).click()

    def clear(self, loc):
        """点击"""
        self.loctor(loc).clear()

    def get_url(self, url):
        self.driver.get(url)


