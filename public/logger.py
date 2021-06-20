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
    print(log_path)

    def __init__(self, filename=log_path, level='info', when='D', backCount=3,
                 fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        self.logger.handlers.clear()   # 清理已经存在的handler，防止日志重复
        format_str = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        sh = logging.StreamHandler() # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount,
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


if __name__ == '__main__':
    logger = Logger().logger
    message = "信息info:测试一下by test"
    logger.info(message)
