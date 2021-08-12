#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : exec_pytest.py
@Author  : liuzhiming
@Time    : 2021/5/27 19:22
"""

import os
from utils.common import *
from selenium import webdriver
from config.path_conf import path_join


# 结果数据，报告不备份
def exec_command(command):
    path_list = ["venv", "Scripts", "activate.bat"]
    venv_path = path_join(path_list)
    # 防止在cmd中显示乱码
    os.system('CHCP 65001')
    os.system("{0} && {1} ".format(venv_path, command))
    # os.popen("{0} && {1} ".format(venv_path, command))


def gen_allure(mark=None, kw=None):

    xml_path = path_join(["report", "allure-xml"])
    result_path = path_join(["report", "allure-result"])
    # 主动清理历史数据，--clean不生效，不知道原因
    os.system("rmdir /s/q {0}".format(result_path))   # 清理报告数据
    os.system("rmdir /s/q {0}".format(xml_path))   # 清理结果数据
    # generate_command = "allure generate {0} -o {1} --clean".format(xml_path, result_path)
    generate_command = "allure generate {0} -o {1}".format(xml_path, result_path)
    # allure serve data_path = allure open
    open_command = "allure open {0}".format(result_path)
    html_name = "./report/{0}".format(get_time())

    test_command = "pytest -v -s --alluredir={0}".format(xml_path)
    if mark is not None:   # 执行某个标签的用例
        test_command = "pytest -v -s -m {} --alluredir={}".format(mark, xml_path)
    elif kw is not None:    # 执行包含某个关键字的用例
        test_command = 'pytest -v -s -k "{}" --alluredir={}'.format(kw, xml_path)

    exec_command(test_command)
    exec_command(generate_command)
    exec_command(open_command)


def gen_html(mark=None, kw=None):
    html_name = get_current_project_path() + "\\report\\{0}".format(get_time()+".html")
    command = "pytest -v -s --html={0}".format(html_name)
    if mark is not None:
        command = "pytest -v -s -m {1} --html={0}".format(html_name, mark)
    elif kw is not None:
        command = 'pytest -v -s -k "{1}" --html={0}'.format(html_name, kw)
    print(command)
    exec_command(command)
    # 自动调用chrome，打开测试报告
    driver = webdriver.Chrome()
    driver.get(html_name)


if __name__ == '__main__':
    # gen_html()
    gen_allure(mark="demo")
