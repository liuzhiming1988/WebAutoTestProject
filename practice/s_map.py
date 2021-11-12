#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : s_map.py
@Author  : liuzhiming
@Time    : 2021/11/8 16:42
"""
import random
from concurrent.futures import ThreadPoolExecutor
import time
import multiprocessing as m
Exception

print("本机CPU核心数：{}个".format(m.cpu_count()))


def get_num(num):
    stop = random.randint(1, 5)
    time.sleep(stop)
    a = random.randint(5, 99)
    print("{} * {} = {}".format(num, a, num*a))
    return a*num


# 将序列中的每个元素都执行同一个函数
nums = [1, 2, 3, 4, 5]
# t1 = time.time()
# for data in map(get_num, nums):
#     print(data)
# t2 = time.time()
# print("耗时：{}s".format(t2-t1))

executor = ThreadPoolExecutor(max_workers=5000)
t3 = time.time()
for data in executor.map(get_num, range(10000)):
    pass

t4 = time.time()
print("耗时：{}s".format(t4-t3))

