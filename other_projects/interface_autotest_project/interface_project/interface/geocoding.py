#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

import json
import urllib.parse

from globalpkg.log import logger
from unittesttestcase import MyUnittestTestCase
from interface.ipquery import IPQuery

class GeoCoding(MyUnittestTestCase):
   def setUp(self):
       pass

   def test_get_ip_info(self):
       #global step_output
       # step_output = step_output.output
       '''演示步骤之间存在依赖(前一步骤的输出为后一步骤的是输入)的情况'''

       logger.info('正在发起GET请求...')

       step_output = IPQuery.step_output
       step_output = step_output.split('localAddress=')[1]
       step_output = step_output.split(',')[0]
       step_output = step_output.split(':')[1]
       step_output = step_output.replace('\"', '')

       self.params = (self.params)[0]
       self.params['a'] = step_output

       self.params = urllib.parse.urlencode(self.params)

       response = self.http.get(self.url, self.params)

       logger.info('正在解析返回结果')

       json_response = json.loads(response.decode('utf-8'))  #如果有必要，用decode函数对获取的字节数据进行解码

       self.assertEqual(json_response['lat'],  self.expected_result['lat'], msg='lat值错误')
       self.assertEqual(json_response['lon'],  self.expected_result['lon'], msg='lon值错误')

   def tearDown(self):
       pass