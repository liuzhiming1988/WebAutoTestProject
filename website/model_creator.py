#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : model_creator.py
@Author  : liuzhiming
@Time    : 2021/7/30 11:42
"""

"""model生成器"""

import os
from utils.common import *
from selenium import webdriver
from config.path_conf import path_join
import json


def exec_venv_command(command):
    """
    激活venv后，再执行命令
    :param command:
    :return:
    """
    path_list = ["venv", "Scripts", "activate.bat"]
    venv_path = path_join(path_list)

    # os.system('CHCP 65001') # 防止在cmd中显示乱码
    res = os.system("{0} && {1} ".format(venv_path, command))
    if res == 0:
        return True
    else:
        return False


def model_creator(table_name):
    """
     根据数据库表，自动创建model文件
    :param table_name: 表名
    :return:
    """
    path_list = ["website", "models"]
    file_path = path_join(path_list)
    command = 'flask-sqlacodegen "mysql+pymysql://root:123456@10.0.11.14:3306/autotest" ' \
              '--tables {} --outfile "{}/{}.py" --flask'.format(table_name, file_path, table_name)
    if exec_venv_command(command):
        return True
    else:
        return False


tables = ["db_info"]
error_list = []
for t in tables:
    if model_creator(t):
        pass
    else:
        err_info = {
            "table": t,
            "err_str": "modle创建失败"
        }

        error_list.append(err_info)
print(json.dumps(error_list, indent=5, ensure_ascii=False))