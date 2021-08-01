#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : merchant_check.py
@Author  : liuzhiming
@Time    : 2021/7/19 16:04
"""

from apis.hsb_pro_api import HsbProApi
from flask import Blueprint
from flask import Flask
from flask import request
import json
from flask import render_template
from apis.hsb_pro_api import HsbProApi


merchant_check_blue = Blueprint("merchant_check", __name__)


@merchant_check_blue.route("/merchant_check", methods=['GET', 'POST'])
def merchant_check():
    # text = "<h3>专业版-商家自检-精准发布：</h3><br />"
    text = ""
    if request.method == "POST":
        phone = request.form.get("phone")
        sms_code = request.form.get("sms_code")
        brand_id = request.form.get("brand_id")
        product_id = request.form.get("product_id")
        num = request.form.get("num")
        # 对用户提交数据进行基本检查
        if len(phone) == 0 or len(sms_code) == 0:
            phone = "18676702152"
            sms_code = "666666"
        if len(brand_id) == 0 or len(product_id) == 0:
            # 如果没输入品牌ID，则取默认值
            brand_id = "2"
            product_id = "38200"
        if len(num) == 0:
            num = 1
        else:
            num = int(num)

        pro = HsbProApi()
        pro.login(phone, sms_code)
        if pro.mark:
            pro.get_store_list()
            for x in range(num):
                pro.detect_v3_get_sn()
                pro.get_check_option(brand_id, product_id)
                basic_selects = pro.get_basic_selects()
                condition_selects = pro.get_condition_selects()
                function_selects = pro.get_function_selects()
                repair_selects = pro.get_repair_selects()
                pro.save_update_check_result(basic_selects, 1)
                pro.save_update_check_result(condition_selects, 2)
                pro.save_update_check_result(function_selects, 3)
                pro.save_update_check_result(repair_selects, 4)
                pro.product_evaluate_merchant_check()
                pro.save_photo_merchant_check()
                pro.apply_for_create_goods(product_id)
                text += "{}<br /><hr />".format(pro.mark_text)
        else:
            text = pro.mark_text
        # return text

    return render_template("tips.html", text=text)