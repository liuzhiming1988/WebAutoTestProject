#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : config.py
@Author  : liuzhiming
@Time    : 2021/5/21 16:18
@Software: PyCharm
"""
import configparser
import traceback
from selenium import webdriver
import os
from public.common import *


class ConfigRead:

    """定义读取ini配置文件的方法"""
    BASE_DIR = get_current_project_path()  # 获取当前项目的绝对路径
    global_path = os.path.join(BASE_DIR, "config\\config_global.ini")  # 拼接上配置文件路径

    def __init__(self):
        pass

    def get_account(self, name):
        """获取默认用户名和密码"""
        config = configparser.ConfigParser()
        config.read(self.global_path)
        try:
            value = config.get("account", name)
            return value

        except:
            print(traceback.format_exc())

    def get_url(self, name):
        """根据系统名称获取配置文件中的系统地址"""
        config = configparser.ConfigParser()
        config.read(self.global_path)
        try:
            value = config.get('url', name)
            return value

        except:
            print(traceback.format_exc())

    def get_value(self, select, name):
        config = configparser.ConfigParser()
        config.read(self.global_path)
        value = config.get(select, name)
        return value

    def get_value_list(self, select):
        config = configparser.ConfigParser()
        config.read(self.global_path)
        value = config.items(select)
        return value

    def get_all_section(self, select):
        config = configparser.ConfigParser()
        config.read(self.global_path)
        value = config.sections()
        return value

    def get_browser(self):
        if self.get_value("browser", "browser") == "chrome":
            options = webdriver.ChromeOptions()
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            driver = webdriver.Chrome(options=options)
            # 解决日志中此错误--ERROR:device_event_log_impl.cc(214)] [16:59:41.983] Bluetooth: bluetooth_adapter_winrt.cc:1072 Getting Default Adapter failed.
            return driver
        elif self.get_value("browser", "browser") == "firefox":
            return webdriver.Firefox()
        else:
            print("请检查配置，目前只支持chrome和firefox")


if __name__ == '__main__':

    print(ConfigRead().BASE_DIR)
    print(ConfigRead().global_path)
    aa = ConfigRead().get_url("oms")
    bb = ConfigRead().get_account("username")
    cc = ConfigRead().get_value("browser", "browser")
    list1 = ConfigRead().get_value_list("url")

    print(aa)
    print(bb)
    print(cc)
    print(list1[0])
