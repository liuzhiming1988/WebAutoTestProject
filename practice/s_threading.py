#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : s_threading.py
@Author  : liuzhiming
@Time    : 2021/11/9 14:34
"""


import threading


def study_info(*args,**kwargs):
    print(args,kwargs)


def main():
    # 信息列表
    list_info = [{"name":"python 基础","progress":"10%"},
                 {"name": "python 面向对象", "progress": "20%"},
                 {"name": "python 爬虫", "progress": "30%"},
                 {"name": "python pyqt5", "progress": "40%"},
                 {"name": "python 数据结构", "progress": "50%"},]

    # 创建线程
    for i in range(5):
        p = threading.Thread(target=study_info,args=(i,),kwargs=list_info[i])
        # 启动线程
        p.start()


if __name__ == "__main__":

    main()
