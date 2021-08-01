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
from flask import flash
from flask import url_for
from flask import Blueprint
from flask import render_template
from datetime import datetime
from random import randint
import time


home_blue = Blueprint("home", __name__)
# views.config.from_object("setting")

@home_blue.route("/homepage")
def homepage():
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

    return render_template("homepage.html",
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




