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
import yagmail
from utils.config_read import ConfigRead
import json
import hashlib
import inspect
from utils.logger import Logger


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        time.sleep(1)
        end_time = time.time()
        run_time = round(end_time-start_time, 2)
        print("{}--总耗时：{}".format(func.__name__, run_time))
        Logger().logger.info("{}--总耗时：{}".format(func.__name__, run_time))
        return res
    return wrapper


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


def get_img_name(fun_name='img'):
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

def md5_encrypt(str):
    m = hashlib.md5()
    m.update(str.encode("utf-8"))
    return m.hexdigest()


def get_header_json(body, secret_key="ohHmcePiHr2hkXIeBlvleHyfuuSkPP2h", server_id="112002"):
    """
    获取公共头部
    :param body: 传入参数字典
    :param secret_key:
    :param server_id:
    :return:
    """
    data = json.dumps(body) + "_" + secret_key
    headers = {"Content-Type": "application/json;charset=UTF-8",
               "HSB-OPENAPI-SIGNATURE": md5_encrypt(data),
               "HSB-OPENAPI-CALLERSERVICEID": server_id}
    return headers

def get_signData(data):
    """
    回收宝自有sign规则，将所有的参数名进行排序，然后按照参数名+参数值进行拼接，最后拼接上key值，再进行sha1加密（utf-8编码），再hexdigest加密
    :param data: 传入一个字典，不包含签名
    :return:
    签名
    """
    signKey = 'b7cab12b2b81385dd2cccb8ce67e4998'
    str1 = ""
    # 将传入的字典进行排序并拼接
    for i in sorted(data):
        # print(i)
        str1 += i+str(data[i])
    # 拼接上key
    str1 += signKey
    # 进行加密
    s = hashlib.sha1()
    s.update(str1.encode("utf-8"))
    sign = s.hexdigest()
    data["sign"]=sign
    return data


def get_method_name():
    """
    获取当前方法的名字
    :return:
    """
    return inspect.stack()[1][3]


if __name__ == '__main__':
    # get_time()

    get_signData({"fds":"trewt"})


