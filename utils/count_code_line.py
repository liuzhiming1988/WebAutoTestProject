#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : count_code_line.py
@Author  : liuzhiming
@Time    : 2021/7/20 14:28
"""

import os


class CountCodeLines:
    """
    统计指定目录下各语言代码行数
    特点：
        1. 按指定类型（后缀名）进行分类统计
        2. 忽略第一级目录中指定的文件夹，如venv文件夹，对统计结果影响很大
    说明：
        1. 类型和忽略目录已经内置，统计目录需进行指定

    """
    def __init__(self):
        self.__BASE_DIR = None
        self.FILE_TYPE_LIST = ["py", "html", "java", "css", "js"]
        self.IGNORE = ["venv", "log", "data"]

    @property
    def base_dir(self):
        return self.__BASE_DIR

    @base_dir.setter
    def base_dir(self, value):

        self.__BASE_DIR = value

    @staticmethod
    def conunt_file_lines(full_path):
        """
        统计单个文件的代码行
        :param full_path: 完整路径
        :return:
        """
        count = 0
        with open(full_path, "rb") as f:
            for line in f.readlines():
                # 判断是否空行
                if line != b"\r\n":
                    count += 1

        return count

    def get_files(self):
        """
        遍历指定目录，筛选出后缀名符合要求的文件名的绝对路径
        :param base_dir:
        :return: 筛选后的文件的列表
        """
        if self.base_dir is None:
            text = "请指定统计目录"
            print(text)
            return False
        file_lists = []
        for parent, folders, files in os.walk(self.base_dir):
            # 在第一次遍历时，将需要忽略的文件夹删掉
            if parent == self.base_dir:
                for x in self.IGNORE:
                    try:
                        folders.remove(x)
                    except Exception as e:
                        print(e)

            for file in files:
                type_ = file.split(".")[-1]
                # 判断文件后缀名，匹配上则将文件完整路径添加到文件列表中，最后返回
                if type_ in self.FILE_TYPE_LIST:
                    full_path = os.path.join(parent, file)
                    file_lists.append(full_path)
        return file_lists

    def count_lines(self):
        """
        统计最终的代码行，并根据不同类型分别统计，返回一个字典
        :return:
        """
        result_dict = {}
        # 构造结果字典，每一个类型为一个key
        for x in self.FILE_TYPE_LIST:
            result_dict[x] = 0

        lists = self.get_files()
        if lists:
            # 统计每一个文件的代码行，并分别累计到对应的key中
            for file in lists:
                type_ = file.split(".")[-1]
                lines = self.conunt_file_lines(file)
                result_dict[type_] += lines
            text = "【{}】统计结果：\n==========================\n" \
                   "文件类型       行数 \n--------------------------\n".format(self.base_dir)
            for x, y in result_dict.items():
                text += "{}           {}行\n--------------------------\n".format(x, y)

            print(text)
            return result_dict


if __name__ == '__main__':
    cc = CountCodeLines()
    cc.base_dir = "D:\\work\\WebAutoTestProject"
    cc.count_lines()
