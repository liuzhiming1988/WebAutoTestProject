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
import datetime
import time
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


# # http://127.0.0.1:5000/user_info/88892
# @app.route("/user_info/<int:id>")
# def user_info(id):
#     return "你输入的是{}".format(id)


# http://127.0.0.1:5000/user/uteds234
@app.route("/user/<string:user_name>")
def user(user_name):
    return "你输入的是{}".format(user_name)

# http://127.0.0.1:5000/demo
@app.route("/demo")
def demo():
    "跳转"
    text = url_for('index')
    print(text)
    return text


# http://127.0.0.1:5000/demo_index
@app.route("/demo_index")
def demo_index():
    "url_for 接收一个参数进行跳转"
    text = url_for('index')
    print(text)
    return redirect(text)


# http://127.0.0.1:5000/demo_info
@app.route("/demo_info")
def demo_info():
    """url_for 接收两个参数"""
    return redirect(url_for("user_info", id=5555))


# http://127.0.0.1:5000/demo1
@app.route("/demo1", methods=["GET", "POST"])
def demo1():
    print(request.method)
    print(request.url)
    return "{}<br>{}<br>OK".format(request.url, request.method)


# http://127.0.0.1:5000/demo3?name=78643
@app.route("/demo3")
def demo3():
    u_name = request.args.get("name")
    return "你提交的名字为：{}".format(u_name)

# 设置cookies
@app.route("/login", methods=["GET", "POST"])
def login():
    res = make_response("successful")
    res.set_cookie("username", "cookie-12345678...")
    return res

@app.route("/get_user_info")
def get_user_info():
    return request.cookies.get("username", "not exists!!!!sfhdkashlehgs")


@app.route('/logout')
def logout():
    response = make_response('退出成功！')
    response.delete_cookie('username')
    return response

# session相关
@app.route('/login2')
def login2():
    session['username'] = 'liuzhiming8888888'
    return '登录成功！'


@app.route('/user_info2')
def user_info2():
    return session.get('username', '用户信息不存在！')


@app.route('/logout2')
def logout2():
    session.pop('username', None) # None参数保证不报错，也就是当pop找不到需要删除的下标的时候会返回None，从而使得不报错。
    return '退出成功！'

# 请求上下文和应用上下文
## 使用g全局临时变量后
# http://127.0.0.1:5000/test_login?username=xiaoming&passwd=111111
@app.route('/test_login')
def test_login():
    username = request.args.get('username')
    passwd = request.args.get('passwd')
    if username == 'xiaoming' and passwd == '111111':
        g.username = username  # 将username赋值给g全局临时变量g下面的一个自定义的属性username
        login_time()
        login_ip()
        return '登录成功！'
    else:
        return '用户名或密码不正确！'


def login_time():
    print('当前登录用户为{}，登录时间为：{}，已写入数据库了！'.format(
        g.username, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    # 我们就可以从g全局临时变量上直接取到g.username的属性，也就是我们在上面赋值的username


def login_ip():
    print('当前登录用户为{}，登录ip为：{}，已写入数据库了！'.format(
        g.username, request.__dict__['environ']['REMOTE_ADDR']))


# 利用 应用上下文current_app 从setting中获取配置项
@app.route('/app_data')
def app_data():
    text = current_app.config['SECRET_KEY']
    print(text)
    return text




if __name__ == '__main__':
    app.run()
