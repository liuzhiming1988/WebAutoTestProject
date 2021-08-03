#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : helloword.py
@Author  : liuzhiming
@Time    : 2021/6/29 下午11:50
"""

from flask import Flask
from flask import redirect
from flask import url_for
from flask import request
from flask import render_template
from flask import make_response
from flask import session
from flask import g
from flask import current_app
from flask import flash
import datetime
from website.views import in_storage
from website.views.home import home_blue
from website.views.new_standard_detect import detect_blue
from website.views.wms_sign import wms_sign_blue
from website.views.outbound_delivery_order import outbound_delivery_order_blue
from website.views.own_place_order import own_place_order_blue
from website.views.merchant_check import merchant_check_blue
from website.views.jw_view import in_storage_blue
from website.views.base_service import base_blue
from website.views.honor_test import honor_blue
from website.setting import TestConfig
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, static_url_path="/static_files",
            static_folder="static_files", template_folder="templates")

app.config.from_object(TestConfig)       # 从setting.py文件中导入TestConfig类
# views.config.from_pyfile('setting.ini')      # 引入.ini的配置文件，主要需要带上后缀名

db = SQLAlchemy(app)

# 注册蓝图
app.register_blueprint(home_blue)
app.register_blueprint(detect_blue)
app.register_blueprint(wms_sign_blue)
app.register_blueprint(outbound_delivery_order_blue)
app.register_blueprint(own_place_order_blue)
app.register_blueprint(merchant_check_blue)
app.register_blueprint(in_storage_blue)
app.register_blueprint(base_blue)
app.register_blueprint(honor_blue)


@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    name = "嘿嘿嘿"
    return render_template("index.html", name=name)

# 异常捕获，捕获404返回码
@app.errorhandler(404)
def error(e):
    error_text = "不存在的页面：<br>{}".format(e)
    return render_template("404.html")


if __name__ == '__main__':
    app.run(port=TestConfig.PORT)
