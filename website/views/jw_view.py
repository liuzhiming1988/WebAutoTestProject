#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : jw_view.py
@Author  : liuzhiming
@Time    : 2021/6/29 下午11:50
"""
from flask import request
from flask import render_template
from website.views import in_storage
from flask import Blueprint

in_storage_blue = Blueprint("jw_view", __name__)


@in_storage_blue.route("/in_storage_jw", methods=['GET', 'POST'])
def in_storage_jw():
    res_text = ""

    if request.method == "POST":

        input_code = request.form.get("bar_code")     # 获取html中提交的参数
        input_code = input_code.strip()          # 去除前后空格
        code_list = input_code.split(",")
        for barCode in code_list:
            res_text += "商品编码【{}】执行结果：<br>".format(barCode)
            if len(barCode) == 18:
                test = in_storage.TestInStorage()
                res_text += test.test_add_storage_order(barCode)
                # 将这个结果返回到页面上
                # flash(res_text)
            else:
                res_text += "错误提示：商品条码的长度应为18，" \
                            "你輸入的条码长度为 {}，输入有误,请检查后重新提交".format(len(barCode))
                # flash(res_text)
            res_text += "<br><br>"

    return render_template("tips.html", text=res_text)
