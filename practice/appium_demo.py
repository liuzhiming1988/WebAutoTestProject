#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : appium_demo.py
@Author  : liuzhiming
@Time    : 2021/11/29 14:50
"""

from appium import webdriver
from appium.webdriver.common.mobileby import By
import json
import time
from base.android_base_page import *


# 如何判断启动成功？  偶尔出现闪退问题如何解决
class LoginPage(AndroidBasePage):
    btn_ok = ("id", "com.hll.phone_recycle:id/btn_dialog_ok", "同意协议按钮")
    btn_skip = ("xpath", "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget"
                         ".FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget"
                         ".RelativeLayout/android.widget.TextView", "跳过引导页")
    close_alert = ("id", "com.hll.phone_recycle:id/ad_dialog_close", "关闭广告弹窗")
    my_module = ("id", "com.hll.phone_recycle:id/navigation_layout5", "我的-主模块")
    value_list = ("id", "com.hll.phone_recycle:id/navigation_layout4", "保值榜-主模块")
    go_login_btn = ("id", "com.hll.phone_recycle:id/user_name_tv", "我的-去登录")
    phone_ipt = ("id", "com.hll.phone_recycle:id/login_phone", "手机号输入框")
    get_sms_btn = ("id", "com.hll.phone_recycle:id/login_timer", "获取验证码按钮")
    sms_code_ipt = ("id", "com.hll.phone_recycle:id/login_pwd", "短信验证码输入框")
    agreement_checkbox = ("id", "com.hll.phone_recycle:id/agreement_checkbox", "勾选同意用户协议")
    login_btn = ("id", "com.hll.phone_recycle:id/login", "登录按钮")

    def start_app(self):
        try:
            if self.find_element(self.btn_ok):
                self.click(self.btn_ok)
                self.click(self.btn_skip)
                time.sleep(3)
            if self.find_element(self.close_alert):
                self.click(self.close_alert)
                self.swipe_up(n=2)
        except Exception as ec:
            self.logger.error(repr(ec))

    def enter_my_module(self):
        self.click(self.my_module)

    def enter_value_list(self):
        self.click(self.value_list)

    def go_login(self):
        self.click(self.go_login_btn)

    def login(self, phone, pwd=""):
        self.send_key(self.phone_ipt, phone)
        self.click(self.get_sms_btn)
        # self.send_key(self.sms_code_ipt, pwd)
        self.click(self.agreement_checkbox)
        time.sleep(15)
        self.click(self.login_btn)


if __name__ == '__main__':
    desired_caps = {"platformName": "Android",  # 平台名称
                    'platformVersion': '7.1.2',  # 系统版本号
                    'deviceName': '127.0.0.1:21503',  # 设备名称。如果是真机，在'设置->关于手机->设备名称'里查看
                    'appPackage': 'com.hll.phone_recycle',  # apk的包名
                    'appActivity': 'com.hll.phone_recycle.activity.AppStartActivity',  # activity 名称
                    "noRest": "True",
                    "fullReset": "False",
                    "printPageSourceOnFindFailure": "true"
                    }

    remote = "http://127.0.0.1:4723/wd/hub"
    driver = get_apk_driver(remote, desired_caps)

    login = LoginPage(apk_driver=driver)
    login.start_app()
    login.enter_value_list()
    login.enter_my_module()
    login.go_login()
    login.login("13049368516")
    time.sleep(20)
    login.quit()

