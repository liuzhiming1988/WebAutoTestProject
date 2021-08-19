#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : create_xls.py
@Author  : liuzhiming
@Time    : 2021/8/17 11:39
"""

import xlwt
import xlrd
import random
import time


class CreateXls:

    def __init__(self):
        self.book = xlwt.Workbook(encoding="utf-8")
        self.name = "test"+time.strftime("%Y%m%d%H%M%S", time.localtime())

    @staticmethod
    def get_time():
        time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
        # 精确到秒20210818110202
        return time_str

    @staticmethod
    def get_rondom_str(num):
        if isinstance(num, int):
            pass
        else:
            try:
                num = int(num)
            except ValueError:
                print("请输入一个数字")
                num = 8
        # 从指定的字符串中随机选中6个字符
        strings = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        random_str = random.sample(strings, num)
        return random_str

    def write(self, title_list, line_num=100, sheet_num=1):
        x = 0
        if isinstance(title_list, list):
            x = len(title_list)
            if x > 0:
                pass
            else:
                return "标题列表不能为空"
        for i in range(sheet_num):
            sheet = self.book.add_sheet('test' + str(i), cell_overwrite_ok=True)
            # 写入标题
            for j in range(x):
                sheet.write(0, j, title_list[j])
            # 循环写入行数据
            for y in range(1, line_num+1):
                # 定义每个列的取值
                sheet.write(y, 0, self.get_time()+"ttt")
                sheet.write(y, 2, self.get_time()+"999")
        self.book.save("d:\{}.xls".format(self.name))


if __name__ == '__main__':
    cx = CreateXls()
    title_list = ["测试ID","标题", "备注"]
    cx.write(title_list, line_num=10, sheet_num=10)




