#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

import  unittest

class MyUnittestTestCase(unittest.TestCase):
    def __init__(self, methodName='runTest', http=None, casestep=None):
        super(MyUnittestTestCase, self).__init__(methodName)
        self.http = http
        self.url = casestep.get_action()['url']
        self.params = casestep.get_action()['params']
        self.testcase_id = casestep.get_tasecase_id()
        self.step_id = casestep.get_step_id()
        self.expected_result = casestep.get_expected_result()