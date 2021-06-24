# -*- coding: utf-8 -*-
# @Time    : 2021/5/20 23:10
# @Author  : liuzhiming
# @Email   : 
# @File    : base_page.py
# @Software: PyCharm
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchFrameException
import os
import time
import sys
from utils.common import *
import traceback
from selenium import webdriver
from utils.logger import Logger
from config.path_conf import *

# 定义寻找元素方法字典
FIND_LIST = {
    # selenium
    'css': By.CSS_SELECTOR,
    'id': By.ID,
    'name': By.NAME,
    'xpath': By.XPATH,
    'link_text': By.LINK_TEXT,
    'class_name': By.CLASS_NAME
}


class BasePage:
    # 封装每个页面共同的属性和方法

    def __init__(self, driver, timeout=30):
        self.driver = driver
        self.logger = Logger().logger
        self.timeout = timeout

    def __elements(self, key, value):
        """

        :param key:
        :param value:
        :return:
        """
        elements = self.driver.find_elements(by=key, value=value)
        return elements

    @timer
    def find_element(self, loc):
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
                WebDriverWait(self.driver, self.timeout, 0.5).until(
                    EC.visibility_of_element_located((FIND_LIST[key], value)))
                elem = self.driver.find_element(FIND_LIST[key], value)
            except TimeoutException as t:
                self.save_img(get_current_function_name())
                self.logger.error("在{0}秒内未定位到元素，定位方法{1}，值{2}\n异常信息：{3}".format(
                    self.timeout, key, value, t))
            except Exception as e:
                self.save_img(get_current_function_name())
                ec = traceback.format_exc()
                self.logger.error("在{0}秒内未定位到元素，定位方法{1}，值{2}\n异常信息：{3} \nInfo：{4}".format(
                    self.timeout, key, value, e.__class__, ec))

        else:
            self.logger.error("请检查定位方法，目前仅支持：{0}".format(FIND_LIST.values()))

        return elem

    # def loctor(self, loc, timeout=15):
    #     """
    #     元素定位
    #
    #     :arg:
    #      - loc - 传入一个元组，如input = (By.ID, "kw")
    #     :return:
    #      - 返回元素对象
    #     """
    #     self.logger.info("开始寻找元素{0}".format(loc))
    #     WebDriverWait(self.driver, timeout, 0.5).until(EC.visibility_of_element_located(loc))
    #     self.logger.info("已找到元素{0}".format(loc))
    #     return self.driver.find_element(*loc)

    def send_key(self, loc, value):
        """输入方法"""
        self.logger.info("准备输入数据{0}".format(value))
        element = self.find_element(loc)
        element.clear()
        element.send_keys(value)

    def click(self, loc):
        """点击"""
        self.logger.info("点击元素：".format(loc))
        self.find_element(loc).click()

    def get_url(self, url):
        self.logger.info("打开网址：{}".format(url))
        self.driver.get(url)

    def save_img(self, name="Img"):
        """

        :return:
        """
        img_name = name + '_' + get_time() + ".png"
        img_path = path_join(["screenshot", img_name])
        self.driver.get_screenshot_as_file(img_path)
        self.logger.info("截图成功，保存路径为{0}".format(img_path))

    def scroll_to(self, x=10, y=20):
        js = "window.scrollTo({0}, {1});".format(x, y)
        self.driver.execute_script(js)
        self.logger.info("移动滚动条位置：x={0},y={1}".format(x, y))

    def max_window(self):
        # can not use in Mac
        self.driver.maximize_window()
        self.logger.info("最大化当前页面")

    def refresh(self):
        self.driver.refresh()
        self.logger.info("刷新当前页面")
        time.sleep(2)

    def switch_to_frame(self, frame):
        self.driver.switch_to.frame(frame)
        self.logger.info("<===============>进入frame:{}".format(frame))

    def switch_to_default_frame(self):
        """返回默认的frame"""
        self.logger.info("跳转回默认的iframe")
        try:
            self.driver.switch_to.default_content()
        except Exception as e:
            self.logger.error("跳转默认iframe失败，error:{}".format(e))

    def is_alert_exist(self):
        """
        assert alert if exist
        :return: alert obj
        """
        self.logger.info("assert alert if exist")
        try:
            re = WebDriverWait(self.driver, self.timeout).until(EC.alert_is_present())
        except NoAlertPresentException:
            return False
        except Exception:
            return False

        return re


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


if __name__ == '__main__':
    keys = FIND_LIST.keys()
    for x in keys:
        print(x)

    # print(keys)

