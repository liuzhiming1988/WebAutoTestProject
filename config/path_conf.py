#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : path_conf.py
@Author  : liuzhiming
@Time    : 2021/6/20 下午9:35
"""

import os


def path_join(path_list):
    """
    In order to make the file path compatible with Mac and windows at the same time,
    os.path.join() method is used to splice the paths,
    :param path_list: For example: ["config", "path_conf.py"]
    :return:Full path
    """
    full_path = os.path.abspath(os.path.dirname(__file__)).split('WebAutoTestProject')[0]+'WebAutoTestProject'
    for x in path_list:
        full_path = os.path.join(full_path, x)
    return full_path


if __name__ == '__main__':

    l = ["data", "value_oms_login.xls"]
    print(path_join(l))
    # output on Mac: /Users/liuzhiming/Documents/autotest/WebAutoTestProject/data/value_oms_login.xls

