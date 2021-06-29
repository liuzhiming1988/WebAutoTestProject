#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : helloword.py
@Author  : liuzhiming
@Time    : 2021/6/29 下午11:50
"""

from flask import Flask
from website import default_config


app = Flask(__name__, static_url_path="/s", static_folder="static_files")

app.config.from_object(default_config.DefaultConfig)


@app.route("/")
def index():
    print(app.config["AUTHOR"])
    return "我的第一个flask程序"


if __name__ == '__main__':
    app.run()
