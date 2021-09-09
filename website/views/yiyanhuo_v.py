#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : yiyanhuo_v.py
@Author  : liuzhiming
@Time    : 2021/8/27 11:30
"""

from apis import idle_fish_api
from flask import Blueprint
from flask import render_template
from flask import request
from flask import jsonify
import json
import time
from apis.honor_data import *

fish_blue = Blueprint("yiyanhuo_v", __name__)

@fish_blue.route("/yiyanhuo", methods=["get","post"])
def yiyanhuo_index():
    return render_template("fish_yanhuo_test.html")


@fish_blue.route("/yiyanhuo_post", methods=["GET", "POST"])
def yiyanhuo_post():
    response = ""
    if request.method == "POST":
        url = request.form.get("interface")
        param = request.form.get("param")

        if len(url) > 0 and len(param) > 0:
            try:
                param = json.loads(param)
                fish = idle_fish_api.FishApi()
                response = fish._post(url, param)
            except json.JSONDecodeError as e:
                response = "参数有误，必须传入json格式，请检查您的输入！！！"
        else:
            response = "接口地址和接口参数不能为空！"
        return response
    else:
        return render_template("fish_yanhuo_test.html")