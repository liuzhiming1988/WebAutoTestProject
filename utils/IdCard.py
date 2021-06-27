#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : IdCard.py
@Author  : liuzhiming
@Time    : 2021/6/18 下午6:39
"""

from utils.address_dict import ADDRESS_DICT
from random import randint
import random
import time
"""
公民身份号码是由17位数字码和1位校验码组成。排列顺序从左至右分别为：6位地址码，8位出生日期码，3位顺序码和1位校验码。

地址码（身份证地址码对照表见下面附录）和出生日期码很好理解，顺序码表示在同一地址码所标识的区域范围内，对同年同月同日出生的人编定的顺序号，顺序码的奇数分配给男性，偶数分配给女性。

身份证最后一位校验码算法如下：

将身份证号码前17位数分别乘以不同的系数，从第1位到第17位的系数分别为：7 9 10 5 8 4 2 1 6 3 7 9 10 5 8 4 2
将得到的17个乘积相加。
将相加后的和除以11并得到余数。
余数可能为0 1 2 3 4 5 6 7 8 9 10这些个数字，其对应的身份证最后一位校验码为1 0 X 9 8 7 6 5 4 3 2。"""


class IDCard:

    def __init__(self):
        # 系数
        self.ratio = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        self.month_list = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
        self.day_list = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
                         "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                         "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]

    @staticmethod
    def get_address_num():
        """
        get a random address number from the address_dict
        :return:
        """
        x = randint(0, 3400)
        # 从地址码字典中随机获取一个地址码，从字典的key中获取，需要将keys转换为list再进行取值
        address_num = list(ADDRESS_DICT.keys())[x]
        # 地址码不足6位时进行补全
        if len(address_num) < 6:
            digit = "0" * (6 - len(address_num))
            address_num += digit
        return address_num

    @classmethod
    def check_leap_year(cls, year):
        """
        check the year is leap year
        :param year:
        :return:
        """
        if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
            return True
        else:
            return False

    def get_date_number(self):
        """
        获取8位出生日期码，随机获取年， 月， 日
        :return:
        """
        year = randint(1900, 2021)
        month = random.choice(self.month_list)
        month = "02"
        if month == "02":
            if self.check_leap_year(year):
                x = randint(0, 28)
                day = self.day_list[x]
            else:
                x = randint(0, 27)
                day = self.day_list[x]
        elif month in ["04", "06", "09", "11"]:
            x = randint(0, 29)
            day = self.day_list[x]
        else:
            x = randint(0, 30)
            day = self.day_list[x]
        res = str(year) + month + day
        return res

    @staticmethod
    def get_digit3():
        """
        获取三位顺序码
        :return:
        """
        a = randint(0, 9)
        b = randint(0, 9)
        c = randint(0, 9)
        num = str(a) + str(b) + str(c)
        # print(num, type(num))
        return num

    def get_digit17(self):
        """

        :return:
        """
        digit17 = self.get_address_num() + self.get_date_number() + self.get_digit3()
        # print(digit17)
        return digit17

    def get_IdCard(self):
        """
        get the check digit,and return the IDCard
        :return:
        """
        str17 = self.get_digit17()
        sum_ = 0
        for x in range(len(str17)):
            sum_ += int(str17[x])*int(self.ratio[x])
        res = sum_ % 11
        if res == 10:
            res = "X"
        res = str(res)
        id_card = str17 + res
        print(id_card)
        return id_card


if __name__ == '__main__':
    # get_address_num()
    # get_date_number()
    # get_digit3()
    IDCard().get_IdCard()


