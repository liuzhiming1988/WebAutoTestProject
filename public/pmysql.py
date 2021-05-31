#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : pmysql.py
@Author  : liuzhiming
@Time    : 2021/5/26 11:03
"""
# 导入pymysql模块
import pymysql
from public.config import ConfigRead


class Pmysql:

    def __init__(self):
        self.conn = pymysql.connect(
            host="127.0.0.1",
            port=3308,
            user="root", password="123456",
            database="test",
            charset="utf8")
        self.cursor = self.conn.cursor()

    def execute_sql(self, sql, limit=10):
        """

        :param sql: 传入要执行的sql语句
        :param limit: 默认限制最多返回10条记录
        :return:
        """
        self.cursor.execute(sql)
        result=None
        if "select" in sql.lower():
            num = self.cursor.rownumber
            count = self.cursor.rowcount
            if count >= limit:
                result = self.cursor.fetchmany(size=limit)
            elif count == 1:
                result = self.cursor.fetchone()
            else:
                result = self.cursor.fetchall()
        else:
            self.conn.commit()
            result = "{0} is success".format(sql)
        self.cursor.close()
        self.conn.close()
        return result

    def close(self):
        self.cursor.close()
        self.conn.close()



