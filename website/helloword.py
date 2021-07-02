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

# app.config.from_object(default_config.DefaultConfig)

@app.route("/")
@app.route("/index", methods=['GET', 'POST'])
def index():
    name = "嘿嘿嘿"
    res_text = ""

    print(request.url)
    print(request.method)

    if request.method == "POST":

        barCode = request.form.get("bar_code")     # 获取html中提交的参数
        if len(barCode) == 18:
            test = in_storage.TestInStorage()
            res_text = test.test_add_storage_order(barCode)    # 将这个结果返回到页面上
        else:
            res_text = "您输入的条码为：【{}】<br><br>错误提示：商品条码的长度应为18，输入有误,请检查后重新提交".format(barCode)
        return res_text

    return render_template("index.html", name=name, res_text=res_text)


if __name__ == '__main__':
    app.run(port=5001, debug=True)
