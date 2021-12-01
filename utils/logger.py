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
import colorlog


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
"""
日志等级：使用范围

FATAL：致命错误
CRITICAL：特别糟糕的事情，如内存耗尽、磁盘空间为空，一般很少使用
ERROR：发生错误时，如IO操作失败或者连接问题
WARNING：发生很重要的事件，但是并不是错误时，如用户登录密码错误
INFO：处理请求或者状态变化等日常事务
DEBUG：调试过程中使用DEBUG等级，如算法中每个循环的中间状态
"""
log_level = ConfigRead().get_log_level()
level_relations = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}  # 定义日志级别

log_name = time.strftime("%Y%m%d", time.localtime()) + ".log"
path_list = ["log", log_name]
log_path = path_conf.path_join(path_list)

class Logger:

    """
    日志类
    """
    fmt = '%(asctime)s - %(pathname)s - %(funcName)s[line:%(lineno)d] - %(levelname)s: %(message)s'

    def __init__(self, when='D', backCount=3):
        self.logger = logging.getLogger(log_path)
        self.logger.handlers.clear()   # 清理已经存在的handler，防止日志重复
        format_str = logging.Formatter(self.fmt)  # 设置日志格式
        self.logger.setLevel(level_relations.get(log_level))  # 设置日志级别
        self.sh = logging.StreamHandler() # 往屏幕上输出
        self.sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        self.th = handlers.TimedRotatingFileHandler(filename=log_path, when=when, backupCount=backCount,
                                               encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        self.th.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(self.sh)  # 把对象加到logger里
        self.logger.addHandler(self.th)


class LoggerV2(object):
    """
    终端打印不同颜色的日志，在pycharm中如果强行规定了日志的颜色， 这个方法不会起作用， 但是
    对于终端，这个方法是可以打印不同颜色的日志的。
    """
    # 在这里定义StreamHandler，可以实现单例， 所有的logger()共用一个StreamHandler
    fmt = '[%(asctime)s] - [%(pathname)s] - %(levelname)s: %(message)s'

    def __init__(self, when='D', backCount=3):
        # if not os.path.exists(self.log_path):        # 如果目录不存在，则创建
        #     os.makedirs(self.log_path)

        self.logger = logging.getLogger(log_path)
        self.logger.handlers.clear()  # 清理已经存在的handler，防止日志重复
        format_str = logging.Formatter(self.fmt)  # 设置日志格式
        self.logger.setLevel(level_relations.get(log_level))  # 设置日志级别
        self.sh = logging.StreamHandler()  # 往屏幕上输出
        # self.sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        self.th = handlers.TimedRotatingFileHandler(filename=log_path, when=when, backupCount=backCount,
                                                    encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        self.th.setFormatter(format_str)  # 设置文件里写入的格式
        # self.logger.addHandler(self.sh)  # 把对象加到logger里
        self.logger.addHandler(self.th)


    def debug(self, message):
        self.fontColor('\033[1;37m%s\033[0m')
        self.logger.debug(message)

    def info(self, message):
        self.fontColor('\033[1;37m%s\033[0m')
        self.logger.info(message)

    def warning(self, message):
        self.fontColor('\033[1;33m%s\033[0m')
        self.logger.warning(message)

    def error(self, message):
        self.fontColor('\033[1;31m%s\033[0m')
        self.logger.error(message, exc_info=True)

    def critical(self, message):
        self.fontColor('\033[1;35;43m%s\033[0m')
        self.logger.critical(message)

    def fontColor(self, color):
        # 不同的日志输出不同的颜色
        formatter = logging.Formatter(color % self.fmt)
        self.sh.setFormatter(formatter)
        self.logger.addHandler(self.sh)


if __name__ == '__main__':
    lg = Logger()
    logger = lg.logger
    # test = lg.level_relations.get("debug")
    # print(test)
    # message = "信息info:测试一下by test"
    # logger.debug(message)
    # logger.error("error:-----")
    # logger.critical("critical------")
    # logger.info("info====")
    logger.warning("warning======")
