#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : own_place_order.py
@Author  : liuzhiming
@Time    : 2021/7/16 19:36
"""

from apis.hsb_app_api import HsbAppApi
from flask import Blueprint
from flask import Flask
from flask import request
import json
from flask import render_template


own_place_order_blue = Blueprint("own_place_order", __name__)


@own_place_order_blue.route("/own_recycle_sf", methods=['GET', 'POST'])
def own_recycle_sf():
    text = "<h1>官方下单-邮寄回收:</h1><br />"
    if request.method == "POST":
        phone = request.form.get("phone")
        sms_code = request.form.get("sms_code")
        num = request.form.get("num")
        product_id = request.form.get("product_id")
        # 对用户提交数据进行基本检查
        if len(phone) == 0 or len(sms_code) == 0:
            phone = "18676702152"
            sms_code = "666666"
        if len(product_id) == 0:
            # 如果没输入品牌ID，则取默认值
            product_id = "38200"
        if len(num) == 0:
            num = 1
        else:
            num = int(num)

        own = HsbAppApi()
        own.login(phone, sms_code)
        if own.mark:
            own.get_service_time()
            own.get_address()
            own.get_store_list()
            for x in range(num):
                own.get_product_param(product_id)
                own.get_select()
                own.get_evaluate(product_id)
                own.get_allow_coupon_list(product_id,5)
                own.get_price_history(product_id)
                own.get_evaluate_result()
                own.place_order_sending()
                text += "{}<br /><hr />".format(own.mark_text)
        else:
            text = own.mark_text
        # return text

    return render_template("tips.html", text=text)
