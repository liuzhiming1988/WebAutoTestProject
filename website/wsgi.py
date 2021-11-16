#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : wsgi.py
@Author  : liuzhiming
@Time    : 2021/11/16 11:44
"""

from flask import Flask


def create_app():

    app = Flask(__name__)
    return app


application = create_app()


if __name__ == '__main__':
    application.run()
