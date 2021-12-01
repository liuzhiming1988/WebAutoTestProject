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

desired_caps = {'platformName': 'Android',  # 平台名称
                'platformVersion': '7.1.2',  # 系统版本号
                'deviceName': '127.0.0.1:21503',  # 设备名称。如果是真机，在'设置->关于手机->设备名称'里查看
                'appPackage': 'com.hll.phone_recycle',  # apk的包名
                'appActivity': 'com.hll.phone_recycle.activity.AppStartActivity',  # activity 名称
                "noRest": True
                }

# print(json.dumps(desired_caps,indent=4))
driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)    # 连接appium
driver.implicitly_wait(5)
# 如何判断启动成功？  偶尔出现闪退问题如何解决
try:
    btn_ok = driver.find_element_by_id("com.hll.phone_recycle:id/btn_dialog_ok")
    if btn_ok:
        btn_ok.click()
        time.sleep(2)
        # driver.find_element_by_id("	com.hll.phone_recycle:id/tv_guide_skip").click()
        driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.TextView").click()

except Exception as ec:
    print(repr(ec))

driver.find_element_by_id("com.hll.phone_recycle:id/navigation_layout5").click()
driver.find_element()
