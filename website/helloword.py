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

@app.route("/", methods=("get", "post"))
@app.route("/index")
def index():
    if request.method == "GET":
        print(app.config["AUTHOR"])
        return render_template("index.html")

    if request.method == "post":
        print("这是一个post请求")
        print(request.headers)
        print(request.json)
        print(request.data)
        barCode = request.form.to_dict()
        print(barCode.get("bar_code"))
        if barCode.get("bar_code") == "123":
            return redirect("/")
    print(request.form.to_dict())



if __name__ == '__main__':
    app.run(port=5001, debug=True)
