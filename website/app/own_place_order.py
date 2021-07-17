#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : own_place_order.py
@Author  : liuzhiming
@Time    : 2021/7/16 19:36
"""

from apis.hsb_app_api import OwnOrder
from flask import Blueprint
from flask import Flask
from flask import request
import json
from flask import render_template


own_place_order_blue = Blueprint("own_place_order", __name__)


@own_place_order_blue.route("/own_place_order", methods=['GET', 'POST'])
def own_place_order():
    text = ""
    if request.method == "POST":
        phone = request.form.get("out_code_list")
        sms_code = request.form.get("out_code_list")
        num = int(request.form.get("out_code_list"))
        if num < 0 or num > 10:
            text = "订单数量需大于0且不能超过10"
        if len(phone) > 0:
            if len(phone) != 11 or phone[0] != 1:
                text = "手机号的长度为11位，且为1开头，请重新输入"
                return text
            if len(sms_code) != 6:
                text = "短信验证码长度应为6位，请重新输入"
                return text
            # 使用输入的账号进行登录下单
        else:
            # 使用默认账号下单
            pass

    return render_template("result.html", text=text)
