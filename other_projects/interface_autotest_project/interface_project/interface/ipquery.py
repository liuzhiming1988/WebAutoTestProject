#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

from globalpkg.log import logger
from globalpkg.globalpy import testdb
from globalpkg.globalpy import case_step_report_tb
from globalpkg.globalpy import executed_history_id
from httpprotocol import MyHttp
from unittesttestcase import MyUnittestTestCase

class IPQuery(MyUnittestTestCase):
   def setUp(self):
       pass

   step_output = None
  # 测试获取省市名称
   def test_get_address_info(self):
       '''演示接口使用host，port，协议和统一配置不一致的时的处理'''

       #global step_output
       myhttp = MyHttp('http', 'ip.ws.126.net', '80')

       logger.info('正在发起GET请求...')
       response = myhttp.get(self.url)

       sql_update = 'UPDATE '+ case_step_report_tb +' SET protocol=\"%s\",host=\"%s\", port=\"%s\"' \
                             'WHERE executed_history_id = %s and testcase_id = %s and step_id = %s' % \
                             ('http', 'ditu.amap.com', '80', executed_history_id, self.testcase_id, self.step_id)
       logger.info('正在更新步骤端口，主机，协议等配置信息: %s' % sql_update)
       testdb.execute_update(sql_update)

       logger.info('正在解析返回结果')
       response = response.decode('gbk')  # decode函数对获取的字节数据进行解码
       IPQuery.step_output = response  # 保存返回结果供其它接口使用
       response = response.split('localAddress=')[1]
       response = response.split(',')[0]
       response = response.split(':')[1]
       response = response.replace('\"', '')

       self.assertEqual(response,  self.expected_result['city_name'], msg='city不为深圳市')


   def tearDown(self):
       pass