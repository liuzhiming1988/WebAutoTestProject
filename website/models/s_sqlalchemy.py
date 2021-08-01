#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : s_sqlalchemy.py
@Author  : liuzhiming
@Time    : 2021/7/28 14:09
"""

from website.setting import TestConfig
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text, Enum
from sqlalchemy.ext.declarative import declarative_base


# print(type(TestConfig.SQLALCHEMY_DATABASE_URI))

# 创建数据库引擎, 创建数据库连接
engine = create_engine(TestConfig.SQLALCHEMY_DATABASE_URI, encoding="utf-8", echo=True, max_overflow=5)
# echo为是否打印结果

# 声明基类
Base = declarative_base()

# 构建数据库表的模型类
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(50))
    create_time = Column(String(50))

    # 可选方法。自定义在显示user对象时的格式
    # def __repr__(self):
    #     return "<User(name='%s', fullname='%s', nickname='%s')>" % (
    #                          self.name, self.fullname, self.nickname)

# 创建表结构
Base.metadata.create_all(engine)   # 数据库有同名表，也不会覆盖

# 添加数据

# 修改数据

# 删除数据

# 删除表

# 查询，多表查询

# 查询前10条，分页

if __name__ == '__main__':
    from sqlalchemy.orm import sessionmaker
    import time

    def add(**kwargs):


        # # print(time_abc)
        # 声明Session类
        Session = sessionmaker(engine)
        # 创建Session对象
        db = Session()
        # 创建User对象，实例化User
        user1 = User(**kwargs)
        # 添加到Session
        db.add(user1)
        # 提交
        db.commit()


    time_abc = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    user2 = ("liuzhiming", "liuzhiming@huishoubao.com.cn", time_abc)
    add(user2)