#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : poexcel.py
@Author  : liuzhiming
@Time    : 2021/5/22 15:44
"""

import xlrd as xr
import xlwt as xw


class PoExcel:
    """定义读取Excel类，读取元素文件"""
    def __init__(self,filename):
        self.filename = filename
        self.file = xr.open_workbook(self.filename)
        self.table = self.file.sheets()[0]  # 取第一个sheet表数据

    def show_details(self):
        # 查看所有sheet列表
        print(self.file.sheet_names())
        sheet1 = self.file.sheets()[0]  # 获得第1张sheet，索引从0开始
        sheet1_name = sheet1.name  # 获得名称
        sheet1_cols = sheet1.ncols  # 获得列数
        sheet1_nrows = sheet1.nrows  # 获得行数
        print('Sheet1 Name: %s\nSheet1 cols: %s\nSheet1 rows: %s' % (sheet1_name, sheet1_cols, sheet1_nrows))
        # 获取指定行数据
        print(sheet1.row_values(0))
        # 获得指定列数据
        print(sheet1.col_values(0))
        # 获得指定单元格数据
        print(sheet1.row(1)[3].value)
        # 获取第一个sheet表格
        table = self.file.sheets()[0]
        # 通过索引顺序获取
        table = self.file.sheet_by_index(0)
        # 通过sheet名称获取
        table = self.file.sheet_by_name(sheet_name='Sheet1')
        # 获取工作薄中所有的sheet名称
        names = self.file.sheet_names()

        # 获取sheet中有效行数
        row = table.nrows
        print(row)
        # 获取sheet中有效列数
        col = table.ncols
        print(col)

        # 返回该行的有效单元格长度
        num = table.row_len(0)
        print(num)

        # rowx表示是获取第几行的数据
        # start_col表示从索引为多少开始，end_colx表示从索引为多少结束，
        # end_colx为None表示结束没有限制
        # 获取指定行中的数据并以列表的形式返回
        table_list = table.row_values(rowx=0, start_colx=0, end_colx=None)
        print(table_list)

        # colx表示是获取第几列的数据
        # start_rowx表示从索引为多少开始，end_rowx表示从索引为多少结束，
        # end_rowx为None表示结束没有限制
        # 获取指定列中的数据并以列表的形式返回
        table_list = table.col_values(colx=0, start_rowx=0, end_rowx=None)
        print(table_list)

        # 获取指定单元格内的值
        value = table.cell_value(rowx=0, colx=1)
        print(value)

        """python读取excel中单元格的内容返回的有5种类型。ctype: 0
        empty, 1
        string, 2
        number, 3
        date, 4
        boolean, 5
        error。即date的ctype = 3，这时需要使用xlrd的xldate_as_tuple来处理为date格式，先判断表格的ctype = 3
        时xldate才能开始操作。"""
        value = table.cell_type(rowx=0, colx=1)
        print(value)

    def get_every_values(self):
        # 打开工作薄
        # workbook = xr.open_workbook(self.filename)
        # 获取第一个sheet表格
        table = self.file.sheets()[0]
        # 获取行数
        rows = table.nrows
        # 获取列数
        cols = table.ncols
        # 循环获取每行的数据
        for row in range(rows):
            for col in range(cols):
                value = table.cell_value(row, col)
                print('第{}行{}列的数据为：{}'.format(row, col, value))

    def get_cell_value(self, rowx, colx):
        return self.table.cell_value(rowx, colx)

    def get_vaild_data(self, key_col=0, start_index=1, end_index=4):
        """

        :param key_col: 决定用例是否跳过的列
        :param start_index:
        :param end_index:
        :return:
        """

        rows = self.table.nrows  # 获取总行数
        args_list = self.table.row_values(0,start_index,end_index)
        value_list = []
        for x in range(1,rows):
            if self.get_cell_value(x, key_col) == "yes":
                print("跳过第{0}行数据".format(x))
            else:
                l = self.table.row_values(x, start_index, end_index)
                l.insert(0, x) # 将行号插入，方便后边写入数据时可以获得索引
                value_list.append(l)

        return args_list, value_list


if __name__ == '__main__':
    path ="..\\"+"\\data\\value_oms_login.xls"
    dd=PoExcel(path)
    dd.show_details()
    dd.get_every_values()
    print(dd.get_vaild_data())
    print(dd.get_vaild_data()[0])
    print(dd.get_vaild_data()[1])

