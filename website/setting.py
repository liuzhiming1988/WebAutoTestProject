#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : setting.py
@Author  : liuzhiming
@Time    : 2021/6/30 上午12:18
"""


class BaseConfig:
    pass


class TestConfig(BaseConfig):
    # 服务相关
    DEBUG = False
    PORT = "8888"
    SECRET_KEY = "sessKKW234ERGF781413"

    # 数据库相关配置mysql
    HOSTNAME = '10.0.11.14'
    DB_PORT = '3306'
    DATABASE = 'autotest'
    USERNAME = 'root'
    PASSWORD = '123456'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8mb4".format(
        username=USERNAME, password=PASSWORD, host=HOSTNAME, port=DB_PORT, db=DATABASE)
    SQLALCHEMY_ECHO = False  # 调试开关
    SQLALCHEMY_POOL_SIZE = 10  # 数据库池的大小
    SQLALCHEMY_POOL_TIMEOUT = 15  # 连接超时时间
    SQLALCHEMY_POOL_RECYCLE = 6000  # 自动回收连接的秒数
    SQLALCHEMY_MAX_OVERFLOW = 10  # 控制在连接池达到最大值后可以创建的连接数。当这些额外的 连接回收到连接池后将会被断开和抛弃。
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。

    JSON_AS_ASCII = False


class WorkConfig(BaseConfig):
    pass

# class Config:
#     # mysql+pymysql://user:password@hostip:port/databasename
#     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://hjx:123456@118.89.43.123:3306/test_temp'
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


