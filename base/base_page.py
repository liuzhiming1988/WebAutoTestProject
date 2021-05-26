# -*- coding: utf-8 -*-
# @Time    : 2021/5/20 23:10
# @Author  : liuzhiming
# @Email   : 
# @File    : base_page.py
# @Software: PyCharm
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time
import sys
from public.common import *
import traceback
from selenium import webdriver

FIND_LIST = {
    # selenium
    'css': By.CSS_SELECTOR,
    'id': By.ID,
    'name': By.NAME,
    'xpath': By.XPATH,
    'link_text': By.LINK_TEXT,
    'class_name': By.CLASS_NAME,
}

class BasePage:
    # 封装每个页面共同的属性和方法

    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    def __elements(self, key, value):
        """

        :param key:
        :param value:
        :return:
        """
        elements = self.driver.find_elements(by=key, value=value)
        return elements

    def find_element(self, loc, timeout=3):
        """

        :param loc:
        :param timeout:
        :return:
        """
        key = loc[0]
        value = loc[1]
        elem = 0

        if key in FIND_LIST.keys():

            try:
                self.logger.info(">>>开始寻找元素:定位方法{0}，值{1}".format(key, value))
                if key == 'id':
                    WebDriverWait(self.driver, timeout, 0.5).until(EC.visibility_of_element_located((By.ID, value)))
                    elem = self.driver.find_element(By.ID, value)
                elif key == 'name':
                    WebDriverWait(self.driver, timeout, 0.5).until(EC.visibility_of_element_located((By.NAME, value)))
                    elem = self.driver.find_element(By.NAME, value)
                elif key == 'xpath':
                    WebDriverWait(self.driver, timeout, 0.5).until(EC.visibility_of_element_located((By.XPATH, value)))
                    elem = self.driver.find_element(By.XPATH, value)
                self.logger.info("成功定位元素:定位方法{0}，值{1}".format(key, value))
            except Exception as e:
                self.save_img(get_current_function_name())
                ec = traceback.format_exc()
                self.logger.error("在{0}秒内未定位到元素，定位方法{1}，值{2}\n异常：{3} \nInfo：{4}".format(timeout, key, value, e.__class__, ec))

        else:
            self.logger.error("请检查定位方法，目前仅支持：{0}".format(FIND_LIST.values()))

        return elem

    def loctor(self, loc, timeout=15):
        """
        元素定位

        :arg:
         - loc - 传入一个元组，如input = (By.ID, "kw")
        :return:
         - 返回元素对象
        """
        self.logger.info("开始寻找元素{0}".format(loc))
        WebDriverWait(self.driver, timeout, 0.5).until(EC.visibility_of_element_located(loc))
        self.logger.info("已找到元素{0}".format(loc))
        return self.driver.find_element(*loc)

    def send_key(self, loc, value):
        """输入方法"""
        self.find_element(loc).clear()
        self.find_element(loc).send_keys(value)
        self.logger.warning("输入数据{0}".format(value))

    def click(self, loc):
        """点击"""
        self.find_element(loc).click()

    def get_url(self, url):
        self.driver.get(url)

    def save_img(self, name="Img"):
        """

        :return:
        """
        img_path=get_current_project_path() + "\\screenshot\\" + name + '_' + get_time() + ".png"
        self.driver.get_screenshot_as_file(img_path)
        self.logger.info("截图成功，保存路径为{0}".format(img_path))

    def scroll_to(self, x=10, y=20):
        js = "window.scrollTo({0}, {1});".format(x, y)
        self.driver.execute_script(js)
        self.logger.info("移动滚动条位置：x={0},y={1}".format(x, y))

    def max_window(self):
        self.driver.maximize_window()
        self.logger.info("最大化当前页面")

    def refresh(self):
        self.driver.refresh()
        self.logger.info("刷新当前页面")
        time.sleep(2)



# 常用键盘操作
"""
Keys.BACK_SPACE：删除键
Keys.SPACE：空格键
Keys.TAB：Tab键
Keys.ESCAPE：回退键
Keys.ENTER：回车键
Keys.CONTROL,”a”：组合键，Ctrl + A
Keys.CONTROL,”x”：组合键，Ctrl + X
Keys.CONTROL,”v”：组合键，Ctrl + V
Keys.CONTROL,”c”：组合键，Ctrl + C
Keys.F1：F1键
Keys.F12：F12键
"""

# 鼠标事件
"""
webdriver.ActionChains(driver).context_click("右击的元素定位").perform() #右击事件
webdriver.ActionChains(driver).double_click("双击的元素定位").perform() #双击事件
webdriver.ActionChains(driver).drag_and_drop("拖动的起点元素", "拖动的终点元素").perform() #拖动事件
"""


