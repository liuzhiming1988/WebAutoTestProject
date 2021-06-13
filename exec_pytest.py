#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : exec_pytest.py
@Author  : liuzhiming
@Time    : 2021/5/27 19:22
"""

import os
from public.common import *
from selenium import webdriver


# 结果数据，报告不备份
def exec_command(command):
    venv_path = get_current_project_path() + "\\venv\\Scripts\\activate.bat"
    os.system('chcp 65001')
    os.system("{0} && {1} ".format(venv_path, command))


def gen_allure(mark=None, kw=None):
    res_path = get_current_project_path() + "\\report\\result\\"
    report_path = get_current_project_path() + "\\report\\html\\"
    # 主动清理历史数据，--clean不生效，不知道原因
    os.system("rmdir /s/q {0}".format(report_path))   # 清理报告数据
    os.system("rmdir /s/q {0}".format(res_path))   # 清理结果数据
    generate_command = "allure generate {0} -o {1} --clean".format(res_path, report_path)
    open_command = "allure open {0}".format(report_path)
    html_name = "./report/{0}".format(get_time())

    command = "pytest -v -s --alluredir={0} && {1}".format(res_path, generate_command)
    if mark is not None:   # 执行某个标签的用例
        command = "pytest -v -s -m {2} --alluredir={0} && {1}".format(res_path, generate_command, mark)
    elif kw is not None:    # 执行包含某个关键字的用例
        command = 'pytest -v -s -k "{2}" --alluredir={0} && {1}'.format(res_path, generate_command, kw)

    print(command)
    exec_command(command)
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
    gen_allure(mark="webtest")