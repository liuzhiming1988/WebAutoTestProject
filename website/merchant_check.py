#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : merchant_check.py
@Author  : liuzhiming
@Time    : 2021/7/3 11:01
"""

from flask import Flask
from flask import request
from flask import render_template
from flask import redirect


app = Flask(__name__)
app.config.from_object("setting")       # 引入.py的配置文件

@app.route("/")
@app.route("/test/<id>")
def user_info(id):
    return "你输入的是{}".format(id)




if __name__ == '__main__':
    app.run()
