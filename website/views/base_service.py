#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : base_service.py
@Author  : liuzhiming
@Time    : 2021/7/29 15:57
"""

from flask import Blueprint
from flask import request
from flask import url_for
from flask import redirect
from flask import g
from flask import make_response
from flask import render_template
from flask import session


base_blue = Blueprint("base_service", __name__)

# # http://127.0.0.1:5000/user_info/88892
# @views.route("/user_info/<int:id>")
# def user_info(id):
#     return "你输入的是{}".format(id)


# http://127.0.0.1:5000/user/uteds234
@base_blue.route("/user/<string:user_name>")
def user(user_name):
    return "你输入的是{}".format(user_name)

# http://127.0.0.1:5000/demo
@base_blue.route("/demo")
def demo():
    "跳转"
    text = url_for('index')
    print(text)
    return text


# http://127.0.0.1:5000/demo_index
@base_blue.route("/demo_index")
def demo_index():
    "url_for 接收一个参数进行跳转"
    text = url_for('index')
    print(text)
    return redirect(text)


# http://127.0.0.1:5000/demo_info
@base_blue.route("/demo_info")
def demo_info():
    """url_for 接收两个参数"""
    return redirect(url_for("user_info", id=5555))


# http://127.0.0.1:5000/demo1
@base_blue.route("/demo1", methods=["GET", "POST"])
def demo1():
    print(request.method)
    print(request.url)
    return "{}<br>{}<br>OK".format(request.url, request.method)


# http://127.0.0.1:5000/demo3?name=78643
@base_blue.route("/demo3")
def demo3():
    u_name = request.args.get("name")
    return "你提交的名字为：{}".format(u_name)

# 设置cookies
@base_blue.route("/login", methods=["GET", "POST"])
def login():
    res = make_response("successful")
    res.set_cookie("username", "cookie-12345678...")
    return res

@base_blue.route("/get_user_info")
def get_user_info():
    return request.cookies.get("username", "not exists!!!!sfhdkashlehgs")


@base_blue.route('/logout')
def logout():
    response = make_response('退出成功！')
    response.delete_cookie('username')
    return response

# session相关
@base_blue.route('/login2')
def login2():
    session['username'] = 'liuzhiming8888888'
    return '登录成功！'


@base_blue.route('/user_info2')
def user_info2():
    return session.get('username', '用户信息不存在！')


@base_blue.route('/logout2')
def logout2():
    session.pop('username', None)
    # None参数保证不报错，也就是当pop找不到需要删除的下标的时候会返回None，从而使得不报错。
    return '退出成功！'

# 请求上下文和应用上下文
## 使用g全局临时变量后
# http://127.0.0.1:5000/test_login?username=xiaoming&passwd=111111
@base_blue.route('/test_login')
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
@base_blue.route('/app_data')
def app_data():
    text = current_app.config['SECRET_KEY']
    print(text)
    return text


# 统计网站浏览次数
# 初始化num变量
# @base_blue.before_first_request
# def set_num():
#     session["num"] = 0


# 每次请求前自动+1
# 限制ip访问，只允许本地和公司网络进行访问
@base_blue.before_request
def add_num():
    client_ip = request.__dict__["environ"]["REMOTE_ADDR"]
    if "10.0." in client_ip or "127.0.0" in client_ip:
        session["num"] += 1
    else:
        return "非公司IP，不允许访问"


@base_blue.route("/get_num")
def get_num():
    num = str(session["num"])
    text = "网站总访问次数为：{}".format(num)
    return text


# # 记录最后一次访问时间
# @base_blue.after_request
# def record_last_time(response):
#     response.set_cookie("time", str(
#         datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
#     return response


# 获取最后一次访问时间
@base_blue.route("/get_last_time")
def get_last_time():
    time_ = str(request.cookies.get("time"))
    time_text = "最后一次访问时间为：{}".format(time_)
    return time_text


# 此过滤器功能：过滤掉列表中大于3的元素
# @base_blue.template_filter('filter_large')  # 自定义过滤器，参数为装装饰器的名称，也就是我们在模板中用的名字
# def filter_large(my_list):
#     new_list = []  # 定义空列表
#     for i in range(len(my_list)):  # 遍历传递过来的列表
#         if my_list[i] <= 10:  # 判断每个元素的值是否小于等于3
#             new_list.append(my_list[i])  # 如果小于等于3则追加到新列表中
#     return new_list  # 返回新列表
# Jinja2模板引擎


