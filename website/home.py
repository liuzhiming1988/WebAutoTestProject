#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : home.py.py
@Author  : liuzhiming
@Time    : 2021/7/4 下午4:45
"""

from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from datetime import datetime
from random import randint


app = Flask(__name__)
app.config.from_object("setting")

@app.route("/homepage")
def home():
    my_int = randint(1, 20)
    my_str = "flask is a very good FRAME, DO YOU Know?"
    my_list = ["url_for", "render_template", "redirect", "request", "random"]
    my_int_list = [88, 9, 7, 5, 6, 3, 5]
    my_dict = {"name": "liuzhiming", "age": "18", "money": 88888888}
    my_set = ("set_", "lindan")

    user = {'is_login': True}
    books = [
        {'name': '西游记', 'author': '吴承恩'},
        {'name': '三国演义', 'author': '罗贯中'},
        {'name': '红楼梦', 'author': '曹雪芹'},
        {'name': '水浒传', 'author': '施耐庵'}
    ]

    title = "主页--自动化平台"

    return render_template("home.html",
                           my_int=my_int,
                           my_str=my_str,
                           my_list=my_list,
                           my_dict=my_dict,
                           my_set=my_set,
                           user=user,
                           books=books,
                           title=title,
                           my_int_list=my_int_list
                           )

# 此过滤器功能：过滤掉列表中大于3的元素
@app.template_filter('filter_large')  # 自定义过滤器，参数为装装饰器的名称，也就是我们在模板中用的名字
def filter_large(my_list):
    new_list = []  # 定义空列表
    for i in range(len(my_list)):  # 遍历传递过来的列表
        if my_list[i] <= 10:  # 判断每个元素的值是否小于等于3
            new_list.append(my_list[i])  # 如果小于等于3则追加到新列表中
    return new_list  # 返回新列表






if __name__ == '__main__':
    app.run()

