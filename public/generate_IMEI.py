#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : generate_IMEI.py
@Author  : liuzhiming
@Time    : 2021/6/17 17:09
"""

from random import randint

"""
IMEI为15位数字
格式为AAAAAAAA BBBBBB C
AAAAAAAA 为 Type Allocation Code
BBBBBB 为 Serial Number
C 为 Check Digit
IMEI校验码算法：
(1).将偶数位数字分别乘以2，分别计算个位数和十位数之和
(2).将奇数位数字相加，再加上上一步算得的值
(3).如果得出的数个位是0则校验位为0，否则为10减去个位数
"""


def generate_imei():
    """

    :param number:
    :return:
    """
    num = randint(10000000000000,99999999999999)
    st = str(num)
    odd_sum = 0  # 奇数
    ten_digit = 0  # 个位数之和
    single_digit = 0  # 十位数之和
    for x in range(14):
        if x % 2 == 0:
            odd_sum += int(st[x])  # 奇数位处理
        else:
            num = int(st[x]) * 2
            ten_digit += int(num / 10)  # 偶数位的十位数处理
            single_digit += num % 10   # 偶数位的个位数处理

    # 相加计算最后结果
    res = odd_sum + ten_digit + single_digit
    ass = res % 10
    if ass == 0:
        check_digit = "0"
    else:
        check_digit = str(10-ass)
    imei = st+check_digit
    print(imei)
    return imei

generate_imei()



