# -*- coding: utf-8 -*-
# @Time    : 2021/5/20 23:10
# @Author  : liuzhiming
# @Email   : 
# @File    : base_page.py
# @Software: PyCharm
from selenium import webdriver
from selenium.webdriver.common.by import By

class BasePage:
    # 封装每个页面共同的属性和方法

    def __init__(self,driver):
        self.driver = driver

    # 定位属性方法
    def loctor(self, loc):
        """元素定位"""
        return self.driver.find_element(*loc)

    def send_key(self, loc, value):
        """输入方法"""
        self.loctor(loc).send_keys(value)

    def click(self, loc):
        """点击"""
        self.loctor(loc).click()

    def clear(self, loc):
        """点击"""
        self.loctor(loc).clear()

    def get_url(self, url):
        self.driver.get(url)


