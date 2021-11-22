#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : 102_logger_debug.py
@Author  : liuzhiming
@Time    : 2021/11/22 11:40
"""
import logging
import os
import time
from config import path_conf
from config.config_read import ConfigRead


class logger(object):
    """
    终端打印不同颜色的日志，在pycharm中如果强行规定了日志的颜色， 这个方法不会起作用， 但是
    对于终端，这个方法是可以打印不同颜色的日志的。
    """

    # 在这里定义StreamHandler，可以实现单例， 所有的logger()共用一个StreamHandler
    ch = logging.StreamHandler()

    def __init__(self):
        self.logger = logging.getLogger()
        if not self.logger.handlers:
            # 如果self.logger没有handler， 就执行以下代码添加handler
            self.logger.setLevel(logging.DEBUG)
            path_list = ["log"]
            log_path = path_conf.path_join(path_list)
            log_name = log_path + "\\" + time.strftime("%Y%m%d", time.localtime()) + ".log"
            print(log_name)
            # if not os.path.exists(self.log_path):        # 如果目录不存在，则创建
            #     os.makedirs(self.log_path)

            # 创建一个handler,用于写入日志文件
            fh = logging.FileHandler(log_name, encoding='utf-8')
            fh.setLevel(logging.INFO)

            # 定义handler的输出格式
            self.fmt = '[%(asctime)s] - [%(pathname)s] - %(levelname)s: %(message)s'
            formatter = logging.Formatter(self.fmt)
            fh.setFormatter(formatter)

            # 给logger添加handler
            self.logger.addHandler(fh)

    def debug(self, message):
        self.fontColor('\033[1;37m%s\033[0m')
        self.logger.debug(message)

    def info(self, message):
        self.fontColor('\033[1;32m%s\033[0m')
        self.logger.info(message)

    def warning(self, message):
        self.fontColor('\033[1;33m%s\033[0m')
        self.logger.warning(message)

    def error(self, message):
        self.fontColor('\033[1;31m%s\033[0m')
        self.logger.error(message)

    def critical(self, message):
        self.fontColor('\033[1;35;43m%s\033[0m')
        self.logger.critical(message)

    def fontColor(self, color):
        # 不同的日志输出不同的颜色
        formatter = logging.Formatter(color % self.fmt)
        self.ch.setFormatter(formatter)
        self.logger.addHandler(self.ch)


if __name__ == "__main__":
    logger = logger()
    logger.info("info12345")
    logger.debug("Debug12345")
    logger.warning("Warning12345")
    logger.error("error12345")
    logger.critical("critical123456789")
