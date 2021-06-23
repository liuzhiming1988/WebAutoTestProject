#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : conftest.py
@Author  : liuzhiming
@Time    : 2021/5/27 11:21
"""

import pytest
from selenium import webdriver
from utils.config_read import ConfigRead


@pytest.fixture(scope="function", autouse=True)
def get_driver():
    global driver
    browser = ConfigRead().get_value("browser", "browser")
    driver = None
    print("启动浏览器>>>>>>")
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver = webdriver.Chrome(options=options)
        # 解决日志中此错误--
        # ERROR:device_event_log_impl.cc(214)] [16:59:41.983]
        # Bluetooth: bluetooth_adapter_winrt.cc:1072 Getting Default Adapter failed.
    elif browser == "firefox":
        driver = webdriver.Firefox()
    else:
        print("请检查配置，目前只支持chrome和firefox")
    return driver


@pytest.fixture(scope="function", autouse=True)
def quit_driver():
    yield driver
    driver.quit()
    print(">>>>>>关闭浏览器")
