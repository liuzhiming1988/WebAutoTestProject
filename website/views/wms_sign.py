#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : wms_sign.py
@Author  : liuzhiming
@Time    : 2021/7/14 18:08
"""

from apis.wms_admin import WmsClient
from flask import Blueprint
from flask import Flask
from flask import render_template
from flask import request
import json


wms_sign_blue = Blueprint("wms_sign", __name__)

@wms_sign_blue.route("/wms_sign", methods=['GET', 'POST'])
def wms_sign():
    text = ""
    if request.method == "POST":
        logistics_raw = request.form.get("logistics_num_list")
        if len(logistics_raw) > 0:
            wms = WmsClient()
            wms.get_auth()
            logistics_list = logistics_raw.strip().split(",")
            for logistics_num in logistics_list:
                wms.mark_text = ""
                text += "物流单号：【{}】<br />".format(logistics_num)
                if len(logistics_num.strip()) > 0:
                    try:
                        wms.sign(logistics_num)
                        wms.unpack(logistics_num)
                        wms.receive_search(logistics_num)
                        if wms.mark:
                            wms.get_order_product()
                            wms.get_product_code()
                            wms.bind_order()
                    except Exception as e:
                        wms.logger.error(e)
                    finally:
                        text += wms.mark_text
                else:
                    text += "物流单号输入错误，不能为空！<br /><hr />"
        else:
            text += "请输入正确的数据，不能为空！<br /><hr />"

    return render_template("tips.html", text=text)


