#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : mock_request_file.py
@Author  : liuzhiming
@Time    : 2021/11/4 10:13
"""
# mock学习 待测试接口

import requests


def get_info(url):
    return requests.get(url).status_code


def invoke_get_info(url):
    return get_info(url)


