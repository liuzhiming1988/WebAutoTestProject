#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : test_txt.py
@Author  : liuzhiming
@Time    : 2021/11/15 17:21
"""
import chardet
import codecs
import csv

data = []
new_data = []

with open("d:\host_.txt", "r", encoding="UTF-8") as txt:
    data = txt.readlines()

# print(data)
# 清洗数据，去除空行
for x in range(len(data)):
    t = data[x]
    data[x] = t.strip().strip("\n")
    if len(data[x]) > 0:
        new_data.append(data[x])

with open("d:\\vpc-host.csv", "w", encoding="gbk", newline="") as c:
    writer = csv.writer(c)
    for d in new_data:
        res = d.split(" ")
        # 洗掉每行的空元素
        new_res = []
        for x in res:
            if len(x) > 0:
                new_res.append(x)
        # print(new_res)
        writer.writerow(new_res)

# writerows方法 -》 源数据格式 ([1, 2, 3], [1], [5])






