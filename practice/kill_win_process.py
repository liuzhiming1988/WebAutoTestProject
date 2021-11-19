#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : kill_win_process.py
@Author  : liuzhiming
@Time    : 2021/11/10 11:47
"""

import psutil
import os
import subprocess
import time


def kill_process_by_name(process_name):
    """杀死指定进程"""
    if check_process(process_name):
        n = 0
        while check_process(process_name):
            cmd = "taskkill /F /IM {}".format(process_name)
            popen = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            popen.wait()
            lines = popen.stdout.readlines()
            for line in lines:
                print(line.decode("gbk"))
            n += 1
            time.sleep(2)
            # 为什么要加等待时间，如果不加，程序运行太快，在杀死进程的过程中判断进程还存在，到执行杀死命令时，进程却已经结束，就会报错
        print("执行了{}次".format(n))
    else:
        print("没有找到进程 【{}】".format(process_name))


def check_process(process_name):
    """
    检查指定进程是否存在，存在返回True，不存在返回False
    :param process_name: 进程名，如chrome.exe
    :return: 存在返回True，不存在返回False
    """
    pids = psutil.pids()
    flag = False
    for pid in pids:
        p = psutil.Process(pid)
        if p.name() == process_name:
            flag = True
        else:
            pass
    return flag


def get_all_process():
    """获取所有进程"""
    all_process = os.popen("tasklist").readlines()
    # print(all_process)
    # print(type(all_process[3]))
    for process in all_process:
        print(process)


if __name__ == '__main__':
    #
    kill_process_by_name("firefox.exe")
    kill_process_by_name("chrome.exe")
    # get_all_process()
