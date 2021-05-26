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
import inspect
import traceback


def get_filename():
    """
    获取当前的文件名
    :return:
     - name - 获取到的当前文件名，不带后缀名
    """
    name = os.path.basename(__file__).split(".")[0]
    return name


def get_time():
    """

    :return:
     - time_abc - 返回时间，精确到秒，格式为20210520131421
    """
    time_abc = time.strftime("%Y%m%d%H%M%S", time.localtime())
    return time_abc


def exists_path(pt_name):
    """
    判断某个文件夹是否存在，存在返回true，不存在则创建

    :arg:
     - pt_name - 文件夹路径
    :return:
     - content - 返回一段文字，用于打印到日志中
    """
    res = os.path.exists(pt_name)
    if res:
        content = "目录{0}已存在，自动跳过".format(pt_name)
        print(content)
        return content
    else:
        os.mkdir(pt_name)
        content = "未找到指定目录，已成功创建{0}".format(pt_name)
        print(content)
        return content


def get_current_file_name():
    # 获取当前运行文件的名称，不带后缀名
    # file_name = os.path.basename(__file__).split(".")[0]
    file_name = sys._getframe().f_code.co_name


def get_current_function_name():
    """
    获取当前方法名
    :return:
    """
    # "{0}.{1}".format(self.__class__.__name__, get_current_function_name())
    return inspect.stack()[1][3]


def get_current_project_path():
    """

    :return:
    """
    project_path = os.path.abspath(os.path.dirname(__file__)).split('WebAutoTestProject')[0]
    return project_path+'WebAutoTestProject'


def get_log_name():
    """

    :return:
     - log_name - 定义log文件名，目前规则每天一个log文件，如20210520.log，固定路径为当前项目的log文件夹中
    """
    log_name = get_current_project_path() + "\\log\\" + get_time()[0:8] + ".log"
    return log_name


def get_config_path():
    """

    :return:
    """
    config_path = get_current_project_path() + "\\config\\"
    return config_path


def get_img_name(fun_name = 'img'):
    """

    :arg
     - fun_name - 方法名，可以用get_current_function_name()来获取。默认值img

    :return:

    """

    img_name = get_current_project_path() + "\\screenshot\\" + fun_name + '_' + get_time() + ".png"
    return img_name


def get_error_info():
    content = traceback.format_exc()
    return content


if __name__ == '__main__':
    path_name = get_current_project_path()
    print(path_name)
    full_name = path_name+"\\log\\"+get_time()+".log"
    print(full_name)


