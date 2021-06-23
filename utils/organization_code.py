#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : organization_code.py
@Author  : liuzhiming
@Time    : 2021/6/19 下午4:22
"""
import random

"""
编制规则：
1.全国组织机构代码由八位数字（或大写拉丁字母）本体代码和一位数字（或大写拉丁字母）校验码组成。
本体代码采用系列（即分区段）顺序编码方法。
校验码按照以下公式计算：
C9=11-MOD(∑Ci(i=1→8)×Wi,11)
式中： MOD——代表求余函数；
i——代表代码字符从左至右位置序号；
Ci——代表第i位上的代码字符的值（具体代码字符见附表）；
C9——代表校验码；
Wi——代表第i位上的加权因子；
当C9的值为10时，校验码应用大写的拉丁字母X表示；当C9的值为11时校验码用0表示。
"""


class GetOrgCode:

    def __init__(self):
        self.num_list = list(range(10))    # get a list, value is 1-10
        self.ws = [3, 7, 9, 10, 5, 8, 4, 2]     # weight

    def get_digit8(self):
        """
        Generate an 8-bit random number string
        :return:
        """
        str8 = ""
        for x in range(8):
            str8 += str(random.choice(self.num_list))
        return str8

    def get_org_code(self):
        """
        Calculate the check character and return the organization code
        :return:
        """
        digit8 = self.get_digit8()
        sum_ = 0
        org_code = ""
        for x in range(8):
            sum_ += int(digit8[x])*self.ws[x]
        c9 = 11 - sum_ % 11
        if c9 == 10:
            org_code = "{}-{}".format(digit8, "X")
        else:
            org_code = "{}-{}".format(digit8, str(c9))
        return org_code


if __name__ == '__main__':
    code = GetOrgCode().get_org_code()
    print(code)



