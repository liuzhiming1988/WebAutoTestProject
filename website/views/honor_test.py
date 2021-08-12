#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : honor_test.py
@Author  : liuzhiming
@Time    : 2021/8/3 16:06
"""

from apis.honor import HonorTestApi
from flask import Blueprint
from flask import render_template
from flask import request
from flask import jsonify
import json
import time
from apis.honor_data import *

honor_blue = Blueprint("honor_test", __name__)

@honor_blue.route("/honor", methods=["get","post"])
def honor_index():
    return render_template("honor_test.html")

@honor_blue.route("/get_eg", methods=["get","post"])
def get_eg():
    if request.method == "POST":
        times13 = str(int(time.time() * 1000))
        index = request.form.get("eg_index")
        url_eg = get_eg_url(index)
        param = get_eg_param(index)
        if param["_head"]["_timestamps"]:
            param["_head"]["_timestamps"] = times13
        param = json.dumps(param, indent=4, ensure_ascii=False)
        response = {
            "url": url_eg,
            "param": param
        }
        # return render_template("honor_test_02.html", url=url_eg, param=param)
        return response

    else:
        return render_template("honor_test.html")


@honor_blue.route("/honor_test", methods=["GET", "POST"])
def honor_test():
    response = ""
    if request.method == "POST":
        url = request.form.get("interface")
        param = request.form.get("param")

        if len(url) > 0 and len(param) > 0:
            try:
                param = json.loads(param)
                honor = HonorTestApi()
                response = honor._post(url, param)
            except json.JSONDecodeError as e:
                response = "参数有误，必须传入json格式，请检查您的输入！！！"
        else:
            response = "接口地址和接口参数不能为空！"

        # return render_template("json_response.html", res=response)
        # return render_template("honor_test.html", res=response)
        return response
        # return render_template("tips.html", text=response)
    else:
        return render_template("honor_test.html")


