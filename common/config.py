#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : config.py
@Author  : liuzhiming
@Time    : 2021/5/21 16:18
@Software: PyCharm
"""
import configparser
import traceback


class ConfigRead:

    """定义读取ini配置文件的方法"""
    global_path = """D:\work\WebAutoTestProject\config\config_global.ini"""
    account_path = """D:\work\WebAutoTestProject\config\/account.ini"""

    def __init__(self):
        pass

    def get_account(self, name):
        """获取默认用户名和密码"""
        config = configparser.ConfigParser()
        config.read(self.account_path)
        try:
            value = config.get("account", name)
            return value

        except:
            print(traceback.format_exc())

    def get_url(self, name):
        """根据系统名称获取配置文件中的系统地址"""
        config = configparser.ConfigParser()
        config.read(self.global_path)
        try:
            value = config.get('url', name)
            return value

        except:
            print(traceback.format_exc())


if __name__ == '__main__':
    aa = ConfigRead().get_account("username")
    print(aa)