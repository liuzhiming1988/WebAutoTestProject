#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : locust_script_template.py
@Author  : liuzhiming
@Time    : 2021/10/14 11:23
"""


import random
from locust import SequentialTaskSet, HttpLocust, task

"""
Tips 1: 增加打开文件最大数限制
    机器上的每个HTTP连接打开一个新文件(技术上称为文件描述符)。操作系统可以为可打开的文件的最大数量设置一个较低的限制。如果该限制小于测试中模拟用户的数量，则会发生故障。
    将操作系统的默认最大文件数限制增加到大于你要运行的模拟用户数的数量。如何执行此操作取决于所使用的操作系统。
"""



