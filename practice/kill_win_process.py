#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : kill_win_process.py
@Author  : liuzhiming
@Time    : 2021/11/10 11:47
"""

import psutil
import os


def kill_process_by_name(process_name):
    """杀死指定进程"""
    pids = psutil.pids()
    # print("pids:{}".format(pids))   # 打印所有的pid
    for pid in pids:
        p = psutil.Process(pid)
        # print("P:{}".format(p))    # 打印出每个pid的信息class（psutil.Process(pid=138696, name='Foxmail.exe',
        # status='running', started='09:25:21')）
        if p.name() == process_name:
            cmd = "taskkill /F /IM {}".format(process_name)
            os.system(cmd)

# def check_process():


def get_all_process():
    """获取所有进程"""
    all_process = os.popen("tasklist").readlines()
    # print(all_process)
    # print(type(all_process[3]))
    for process in all_process:
        print(process)


if __name__ == '__main__':
    # kill_process_by_name("chromedriver.exe")
    get_all_process()
