#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : outbound_delivery_order.py
@Author  : liuzhiming
@Time    : 2021/7/15 16:10
"""

from apis.wms_admin import WmsClient
from flask import Blueprint
from flask import Flask
from flask import request
import json
from flask import render_template


outbound_delivery_order_blue = Blueprint("outbound_delivery_order", __name__)


@outbound_delivery_order_blue.route("/outbound_delivery_order", methods=['GET', 'POST'])
def outbound_delivery_order():
    text = ""
    if request.method == "POST":
        out_code_raw = request.form.get("out_code_list")
        out_code_list = out_code_raw.strip().split(",")
        for out_code in out_code_list:
            if len(out_code) > 0:
                text = "<hr /><hr />输入正确"
            else:
                text = "请输入正确的数据，不能为空！"
    return render_template("result.html", text=text)