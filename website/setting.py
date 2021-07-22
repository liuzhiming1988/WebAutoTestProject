#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : setting.py
@Author  : liuzhiming
@Time    : 2021/6/30 上午12:18
"""
import os

DEBUG = False
PORT = 8056
DOMAIN = "10.0.11.172"
# DOMAIN = "127.0.0.1"
SECRET_KEY = "sessKKW234ERGF781413"


# class Config:
#     # mysql+pymysql://user:password@hostip:port/databasename
#     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/study'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SQLALCHEMY_ECHO = True
#     # secret_key
#     SECRET_KEY = 'odfhahsdadsaf5ewr323asf'
#     # 项目路径
#     BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#     # 静态文件夹的路径
#     STATIC_DIR = os.path.join(BASE_DIR, 'static')
#     TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
#     # 头像的上传目录
#     UPLOAD_ICONS_DIR = os.path.join(STATIC_DIR, 'upload\icon')
#     # 相册的上传目录
#     UPLOAD_PHOTOS_DIR = os.path.join(STATIC_DIR, 'upload\photo')
#
#     # flask-session的配置
#     # PERMANENT_SESSION_LIFETIME = timedelta(days=14)	#过期时间
#     SESSION_TYPE = 'redis'								#session选用的数据库
#     SESSION_COOKIE_NAME = 'session_id'					#cookie名字
#
#
# class DevelopmentConfig(Config):
#     ENV = 'development'
#     DEBUG = True

#
# class ProductionConfig(Config):
#     ENV = 'production'
#     DDEBUG = False


