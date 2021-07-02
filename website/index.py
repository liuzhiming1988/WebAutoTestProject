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
from website import in_storage


app = Flask(__name__, static_url_path="/s", static_folder="static_files", template_folder="templates")

app.config.from_object("setting")       # 引入.py的配置文件
# app.config.from_pyfile('setting.ini')      # 引入.ini的配置文件，主要需要带上后缀名

# https://blog.csdn.net/lingjiphp/category_8707067.html
@app.route("/")
@app.route("/index", methods=['GET', 'POST'])
def index():
    name = "嘿嘿嘿"
    res_text = ""

    if request.method == "POST":

        input_code = request.form.get("bar_code")     # 获取html中提交的参数
        input_code = input_code.strip()          # 去除前后空格
        code_list = input_code.split(",")
        for barCode in code_list:
            res_text += "商品编码【{}】执行结果：<br>".format(barCode)
            if len(barCode) == 18:
                test = in_storage.TestInStorage()
                res_text += test.test_add_storage_order(barCode)    # 将这个结果返回到页面上
            else:
                res_text += "错误提示：商品条码的长度应为18，输入有误,请检查后重新提交"
            res_text += "<br><br>"
        return res_text

    return render_template("index.html", name=name, res_text=res_text)


if __name__ == '__main__':
    app.run()
