# -*- coding: utf-8 -*-
# @Time    : 2021/8/1 11:30
# @Author  : liuzhiming
# @Email   : 
# @File    : index.py
# @Software: PyCharm
# import sys
# import os
# curPath = os.path.abspath(os.path.dirname(__file__))
# rootPath = os.path.split(curPath)[0]
# sys.path.append(rootPath)
#


from flask import Flask
from flask import request
from flask import current_app
from flask import make_response
from flask import redirect
from flask import abort
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask import render_template


app = Flask(__name__)
manager = Manager(app)
# bootstrap = Bootstrap(app)


@app.route("/")
@app.route("/index")
def index():
    """
    程序根地址处理程序
    :return:
    """
    user_agent = request.headers.get("User-Agent")  # 从请求头中获取user_agent信息
    headers = request.headers   # 获取请求头内容
    # return "<h1>今天的天气很好！！user-agent:{}  {}</h1>".format(user_agent, headers)
    return render_template("base.html")

# 程序上下文
## current_app
## g
# 请求上下文
## request
## session


@app.route("/user/<name>")
def user(name):
    """
    接收动态参数，并返回
    :param name:
    :return:
    """
    return "hello,{}".format(name)


# 请求钩子
# before_first_request   注册一个函数，在处理第一个请求之前运行
# before_request   注册一个函数，在每次请求之前运行
# after_request    注册一个函数，如果没有未处理的异常抛出，在每次请求之后运行
# teardown_request   注册一个函数，即使有未处理的异常抛出，也在每次请求之后运行


# 返回状态码
@app.route("/status")
def status():
    # 返回的第二个参数，可以定义状态码
    return "返回一个401状态码", 401


# 返回一个response对象
@app.route("/res")
def res():
    response = make_response("make_response:并设置一个cookie")
    response.set_cookie("userId", "13049368516")
    return response


# 重定向特殊响应
@app.route("/redirect/baidu")
def to_baidu():
    "重定向到百度主页"
    return redirect("http://www.baidu.com")


# 特殊响应，处理错误，abort函数生成
@app.route("/getUser/<int:id>")
def get_user(id):
    if id%2 == 0:
        abort(404)
    else:
        return "{}".format(id*2)


# 自定义错误页面
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == '__main__':
    # app.run(debug=True)
    manager.run()

    # python index.py runserver --host 192.168.43.53
    # python index.py runserver --host 127.0.0.1

