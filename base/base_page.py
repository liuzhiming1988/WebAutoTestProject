# -*- coding: utf-8 -*-
# @Time    : 2021/5/20 23:10
# @Author  : liuzhiming
# @Email   : 
# @File    : base_page.py
# @Software: PyCharm
from selenium import webdriver
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
from utils.logger import Logger, LoggerV2
from config.path_conf import *
from utils.ding_rebot import DingRebot

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

"""
元素操作的日志信息基本都使用debug级别，业务相关的使用info级别
"""


class BasePage:
    # 封装每个页面共同的属性和方法

    def __init__(self, driver, timeout=8):
        self.driver = driver
        # self.logger = Logger().logger
        self.logger = LoggerV2()
        self.timeout = timeout

    def find_elements(self, loc):
        """
        定位元素集合
        :param loc:
        :return:
        """
        key = loc[0]
        value = loc[1]
        elements = None

        if key == "xpath":
            pass
        else:
            self.logger.error("find_elements目前仅支持：xpath")

        try:
            self.logger.debug("定位元素：方法【{0}】，值【{1}】".format(key, value))
            WebDriverWait(self.driver, self.timeout, 0.5).until(
                EC.visibility_of_element_located((FIND_LIST[key], value)))
            elements = self.driver.find_elements_by_xpath(value)
        except TimeoutException as t:
            self.save_img(get_current_function_name())
            ec = traceback.format_exc()
            ex_text = "在{0}秒内未定位到元素，定位方法【{1}】，值【{2}】\n异常信息：【{3}】".format(
                self.timeout, key, value, ec)
            DingRebot().send_text(ex_text)
            self.logger.error(ex_text)

        except Exception as e:
            self.save_img(get_current_function_name())
            ec = traceback.format_exc()
            err_text = "在{0}秒内未定位到元素，定位方法{1}，值{2}\n异常信息：{3}".format(
                self.timeout, key, value, e)
            DingRebot().send_text(err_text)
            self.logger.error(err_text)

        return elements

    # @timer
    def find_element(self, loc):
        """
        定位单个元素
        :param loc:
        :param timeout:
        :return:
        """
        time.sleep(0.5)   # 操作之间延时0.5秒，防止点击过快
        key = loc[0]       # 定位方法名
        value = loc[1]      # 元素值
        elem = None
        remark = "默认元素"
        try:
            remark = loc[2]
        except Exception as ec:
            self.logger.warning("未定义元素名称: 〖{0}〗-【{1}】".format(value, repr(ec)))

        if key in FIND_LIST.keys():
            pass
        else:
            self.logger.error("请检查定位方法，目前仅支持：{0}".format(FIND_LIST.values()))
            return False

        self.logger.debug("定位元素【{0}】-〈{1}〉-【{2}】".format(remark, key, value))
        # filename = os.path.split(os.path.abspath(sys.argv[0]))
        try:
            WebDriverWait(self.driver, self.timeout, 0.5).until(EC.visibility_of_element_located((FIND_LIST[key], value)))
            elem = self.driver.find_element(FIND_LIST[key], value)
            return elem

        except TimeoutException as ec:
            self.save_img(get_current_function_name())
            ex_text = "在{0}秒内未定位到元素，定位方法【{1}】，元素：〖{4}〗，值【{2}】\n异常信息：{3}".format(
                self.timeout, key, value, repr(ec), remark)
            # DingRebot().send_text(ex_text)
            self.logger.error(ex_text)
            return False
        except Exception as ec:
            self.save_img(get_current_function_name())
            self.logger.error("在{0}秒内未定位到元素，定位方法【{1}】，值【{2}】\n异常信息：{3} \n".format(
                self.timeout, key, value, repr(ec)))
            return False


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

    @timer
    def send_key(self, loc, value):
        """输入方法"""

        element = self.find_element(loc)
        if element:
            self.logger.debug("输入数据：【{0}】".format(value))
            element.clear()
            element.send_keys(value)

    @timer
    def click(self, loc):
        """点击元素"""
        element = self.find_element(loc)
        if element:
            self.logger.debug("点击元素：【{}】>>【{}】".format(loc[0], loc[1]))
            element.click()

    def implicitly_wait(self, second):
        """隐式等待"""
        self.logger.info("开启隐式等待，时间设置为{}秒".format(second))
        self.driver.implicitly_wait(second)

    def get_url(self, url):
        self.logger.info("打开网址：【{}】".format(url))
        self.driver.get(url)

    def get_elem_text(self, loc):
        element = self.find_element(loc)
        if element:
            text = element.text
            self.logger.debug("获取到的文本为：【{0}】".format(text))
            return text

    def save_img(self, name="Img"):
        """

        :return:
        """
        img_name = name + '_' + get_time() + ".png"
        img_path = path_join(["screenshot", img_name])
        self.driver.get_screenshot_as_file(img_path)
        self.logger.debug("截图成功，保存路径为【{0}】".format(img_path))

    def scroll_to(self, x=10, y=20):
        js = "window.scrollTo({0}, {1});".format(x, y)
        self.driver.execute_script(js)
        self.logger.debug("移动滚动条位置：x={0},y={1}".format(x, y))

    def max_window(self):
        # can not use in Mac
        self.driver.maximize_window()
        self.logger.debug("最大化当前页面")

    def refresh(self):
        self.driver.refresh()
        self.logger.debug("【refresh】刷新当前页面")
        # time.sleep(2)

    def switch_to_frame(self, frame):
        self.logger.debug("进入frame:【{}】".format(frame))
        self.driver.switch_to.frame(frame)
        self.logger.debug("成功进入frame:【{}】".format(frame))


    def switch_to_parent_frame(self):
        self.driver.switch_to.parent_frame()
        self.logger.debug("切换到父级iframe")

    def switch_to_default_frame(self):
        """返回默认的frame"""
        self.logger.debug("跳转回默认的frame")
        try:
            self.driver.switch_to.default_content()
        except Exception as e:
            self.logger.error("跳转默认iframe失败，error:{}".format(e))

    def is_alert_exist(self):
        """
        assert alert if exist
        :return: alert obj
        """
        self.logger.debug("assert alert if exist")
        try:
            re = WebDriverWait(self.driver, self.timeout).until(EC.alert_is_present())
        except NoAlertPresentException:
            return False
        except Exception:
            return False

        return re

    def sleep(self, sleep_time):
        self.logger.info("强制等待 {} 秒".format(sleep_time))
        time.sleep(sleep_time)

    def get_alert_text(self):
        self.sleep(2)
        alert = self.driver.switch_to.alert
        self.sleep(2)
        self.logger.info("弹窗中的文本内容为：【{}】".format(alert.text))
        return alert.text

    def alert_accept(self):
        """在弹出框中点确定，处理alert窗口是不要开多个浏览器，偶尔会导致失败"""
        # 尝试操作弹出框，重试3次，若还失败，捕捉异常，并返回错误
        self.sleep(2)
        self.logger.debug("定位弹出框，点击【确定】按钮")
        for i in range(3):
            try:
                alert = self.driver.switch_to.alert
                self.sleep(1)
                # self.logger.info("弹窗内容：【{}】".format(alert.text))
                alert.accept()
                # self.logger.info("")
                break
            except Exception as e:
                self.logger.error("第{}次在弹出框中点击【确定】按钮失败".format(i))
                self.logger.error("".format(e))
                self.sleep(2)
                i+=1

    def alert_dismiss(self):
        """在弹出框中点取消"""
        self.logger.debug("在弹出框中点击【取消】按钮")
        alert = self.driver.switch_to.alert
        self.sleep(2)
        alert.dismiss()

    def alert_send_key(self, value):
        """在弹出框中输入文本，适合alert-prompt"""
        self.logger.debug("在弹出框中输入文本：【{}】".format(value))
        alert = self.driver.switch_to.alert
        self.sleep(2)
        alert.send_keys(value)

    def exec_script(self, js_str):
        """
        example:
        # 利用js代码块去除自定义弹窗
        js1 = 'document.getElementById('div_company_mini').style.display='none';'
        # div_company_mini为弹窗对应的id
        :param js_str:
        :return:
        """
        self.logger.debug("执行JS语句：【{}】".format(js_str))
        self.driver.execute_script(js_str)


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

