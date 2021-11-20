#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : logger.py
@Author  : liuzhiming
@Time    : 2021/5/24 14:32
"""

import logging
from logging import handlers
from config import path_conf
import time
from config.config_read import ConfigRead


"""
日志级别等级：CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET

format参数中可能用到的格式化串：
%(name)s             Logger的名字
%(levelno)s          数字形式的日志级别
%(levelname)s     文本形式的日志级别
%(pathname)s     调用日志输出函数的模块的完整路径名，可能没有
%(filename)s        调用日志输出函数的模块的文件名
%(module)s          调用日志输出函数的模块名
%(funcName)s     调用日志输出函数的函数名
%(lineno)d           调用日志输出函数的语句所在的代码行
%(created)f          当前时间，用UNIX标准的表示时间的浮 点数表示
%(relativeCreated)d    输出日志信息时的，自Logger创建以 来的毫秒数
%(asctime)s                字符串形式的当前时间。默认格式是 “2003-07-08 16:49:45,896”。逗号后面的是毫秒
%(thread)d                 线程ID。可能没有
%(threadName)s        线程名。可能没有
%(process)d              进程ID。可能没有
%(message)s            用户输出的消息
"""


class Logger:

    """
    日志类
    """
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }    # 定义日志级别

    log_name = time.strftime("%Y%m%d", time.localtime())+".log"
    path_list = ["log", log_name]
    log_path = path_conf.path_join(path_list)
    # print(log_path)
    log_level = ConfigRead().get_log_level()
    fmt = '%(asctime)s - %(pathname)s - %(funcName)s[line:%(lineno)d] - %(levelname)s: %(message)s'

    def __init__(self, when='D', backCount=3):
        self.logger = logging.getLogger(self.log_path)
        self.logger.handlers.clear()   # 清理已经存在的handler，防止日志重复
        format_str = logging.Formatter(self.fmt)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(self.log_level))  # 设置日志级别
        sh = logging.StreamHandler() # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=self.log_path, when=when, backupCount=backCount,
                                               encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(sh)  # 把对象加到logger里
        self.logger.addHandler(th)
        # print("\033[1;36m{}\033[0m".format("Info信息"))
        # print("\033[1;34m{}\033[0m".format("Debug信息"))
        # print("\033[1;37;41m{}\033[0m".format("Error信息"))
        # print("\033[1;31;43m{}\033[0m".format("Warming信息"))


if __name__ == '__main__':
    lg = Logger()
    logger = lg.logger
    # test = lg.level_relations.get("debug")
    # print(test)
    message = "信息info:测试一下by test"
    logger.debug(message)
    logger.error("error:-----")
    logger.critical("critical------")
    logger.info("info====")
    logger.warning("warning======")