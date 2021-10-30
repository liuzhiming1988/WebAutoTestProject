# -*- coding: utf-8 -*-
# @Time    : 2021/10/30 13:38
# @Author  : liuzhiming
# @Email   : 
# @File    : f_sorted.py
# @Software: PyCharm

import operator

list_a = [5, 8, 9, 4, 6, 1]
print(sorted(list_a))   # 新的list
print("list_a的内存地址为:{}".format(id(list_a)))
print("sorted()方法返回了一个新的list，内存地址发生了变化，内存地址为：{}".format(id(sorted(list_a))))
list_a.sort()
# list.sort() 只可以用于list对象
print(list_a)
print("list_a.sort()方法修改的是list本身，内存地址仍为：{}".format(id(list_a)))

# sorted()方法对所有的可迭代序列都有效
res = sorted({1: "A", 4: "A", 3: "A", 9: "A", 8: "A"})
print(res)
# 结果 [1, 3, 4, 8, 9]

# key参数指定一个函数，此函数将在每个月安苏比较前被调用。如下，通过key指定的函数来忽略字符串的大小写
a = sorted("this is a food from china".split(), key=str.lower)
print(a)

# 更为复杂的场景，通过score进行排序，输出name列表
item_list = [
    {
        "score": "88",
        "name": "third"
    },
    {
        "score": "99",
        "name": "first"
    },
    {
        "score": "55",
        "name": "second"
    }
]

names = sorted(item_list, key=lambda score: score["score"], reverse=True)
print(names)
# 结果[{'score': '99', 'name': 'first'}, {'score': '88', 'name': 'third'}, {'score': '55', 'name': 'second'}]













