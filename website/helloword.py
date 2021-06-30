#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : helloword.py
@Author  : liuzhiming
@Time    : 2021/6/29 下午11:50
"""

from flask import Flask
from flask import request
from flask import render_template
from website import default_config


app = Flask(__name__, static_url_path="/s", static_folder="static_files", template_folder="templates")

app.config.from_object(default_config.DefaultConfig)

@app.route("/")
@app.route("/index")
def index():
    print(app.config["AUTHOR"])
    return render_template("index.html")


if __name__ == '__main__':
    app.run(port=5000)
