#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

import time

from globalpkg.log import logger
from globalpkg.mydb import MyDB
from globalpkg.mytestlink import TestLink
from globalpkg.othertools import OtherTools


logger.info('正在初始化数据库[名称：TESTDB]对象')
testdb = MyDB('./config/dbconfig.conf', 'TESTDB')

logger.info('正在获取testlink')
mytestlink = TestLink().get_testlink()

other_tools = OtherTools()

executed_history_id = time.strftime('%Y%m%d%H%M%S', time.localtime())  # 流水记录编号
# testcase_report_tb = 'testcase_report_tb' + str(executed_history_id)
# case_step_report_tb = 'case_step_report_tb' + str(executed_history_id)
testcase_report_tb = 'testcase_report_tb'
case_step_report_tb = 'case_step_report_tb'


