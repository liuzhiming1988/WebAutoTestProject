#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : bangmai_get_high_price.py
@Author  : liuzhiming
@Time    : 2021/9/28 9:44
"""

import math

"""
寄卖预估价格：
真实估价渠道的渠道加成价+展示价规则，取最高价展示给用户

寄卖检测后价格：
回收价：使用真实估价渠道计算回收价
保底价：固定使用10000240渠道计算回收价
最高价：使用真实估价渠道计算回收价+展示价规则，取最高价
"""

recycle_price = 19   # 检测回收价
upper = 20   # 上限
floor = 10  # 下限
high_price_percent = recycle_price*(upper-floor)/100.0*abs(math.sin(recycle_price/100000.0+150))+(recycle_price*(100+floor)/100.0)
high_price_abs = (upper-floor)*abs(math.sin(recycle_price/100000.0+150))+(recycle_price+floor)
print("=======获取闲鱼展示价=======\n检测回收价：{}\n上限：{}\n下限：{}\n最高价为（百分比方式）：{}.00".format(recycle_price,upper,floor,int(high_price_percent)))
print("最高价为（绝对值方式）：{}.00".format(int(high_price_abs)))
print("==========================")


