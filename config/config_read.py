#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : config_read.py
@Author  : liuzhiming
@Time    : 2021/5/21 16:18
@Software: PyCharm
"""
import configparser
import traceback
from selenium import webdriver
import os
from config.path_conf import path_join


class ConfigRead:

    """定义读取ini配置文件的方法"""
    # get path of the config file
    path_list = ["config", "config_global.ini"]
    conf_path = path_join(path_list)
    # print(global_path)

    # add singleton，优化：增加单例模式
    __obj = None
    __init_flag = True

    def __new__(cls, *args, **kwargs):
        if cls.__obj == None:
            cls.__obj = object.__new__(cls)
        return cls.__obj

    def __init__(self):
        if ConfigRead.__init_flag:
            self.config = configparser.ConfigParser()
            self.config.read(self.conf_path, encoding="utf-8-sig")
            ConfigRead.__init_flag = False

    def get_account(self, name):
        """获取默认用户名和密码"""
        # config = configparser.ConfigParser()
        # config.read(self.global_path)
        try:
            value = self.config.get("account", name)
            return value
        except:
            print(traceback.format_exc())

    def get_url(self, name):
        """根据系统名称获取配置文件中的系统地址"""

        try:
            value = self.config.get('url', name)
            return value

        except:
            print(traceback.format_exc())

    def get_value(self, select, name):
        value = self.config.get(select, name)
        return value

    def get_value_list(self, select):
        value = self.config.items(select)
        return value

    def get_all_section(self, select):
        value = self.config.sections()
        return value

    def get_log_level(self):
        level = self.config.get("log", "level")
        return level

    def get_browser(self):
        if self.get_value("browser", "browser") == "chrome":
            options = webdriver.ChromeOptions()
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            driver = webdriver.Chrome(options=options)
            # 解决日志中此错误--ERROR:device_event_log_impl.cc(214)] [16:59:41.983] Bluetooth:
            # bluetooth_adapter_winrt.cc:1072 Getting Default Adapter failed.
            return driver
        elif self.get_value("browser", "browser") == "firefox":
            return webdriver.Firefox()
        else:
            print("请检查配置，目前只支持chrome和firefox")


if __name__ == '__main__':
    cr = ConfigRead()
    print(dir(cr))
    print("==",cr.__dict__)
    print(cr.__doc__)
    print(cr.__class__)
    level = cr.get_log_level()
    print(level)

