#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : common.py
@Author  : liuzhiming
@Time    : 2021/5/22 16:48
"""
import os
import time
import sys


def get_filename():
    """获取当前的文件名"""
    name = os.path.basename(__file__).split(".")[0]
    return name


if __name__ == '__main__':
    get_filename()

