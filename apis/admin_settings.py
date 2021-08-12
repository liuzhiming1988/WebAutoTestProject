#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : admin_settings.py
@Author  : liuzhiming
@Time    : 2021/7/7 16:22
"""


# x-www-form-urlencoded
HEADERS_FORM = {
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
}

# json
HEADERS_JSON = {
    "Content-Type": "application/json;charset=UTF-8"
}

# amc user info
USERNAME_AMC = """test_liuzhiming@huishoubao.com.cn"""
PASSWORD_AMC = "f6758a4e"


# amc
PROTOCAL_AMC = "http"
DOMAIN_AMC = "apicase-amc.huishoubao.com.cn"


# wms
PROTOCAL_WMS = "http"
DOMAIN_WMS = "wms-wwwapi.huishoubao.com.cn"

# detection
PROTOCAL_DETECTION = "http"
DOMAIN_DETECTION = "detection-wwwapi.huishoubao.com/apicase"