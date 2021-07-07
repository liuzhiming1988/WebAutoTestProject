#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

import json
import time

from globalpkg.log import logger
from globalpkg.globalpy import other_tools
from globalpkg.globalpy import case_step_report_tb
from globalpkg.globalpy import executed_history_id
from globalpkg.globalpy import testdb
from casestep import CaseStep

class TestCase:
    def __init__(self, testcase_id, testcase_name, steps, active_status, testproject):
        self.testcase_id = testcase_id
        self.testcase_name = testcase_name
        self.steps = steps
        self.active_status = active_status # 用例是否禁用 1 - 活动 0 - 禁用
        self.testproject = testproject

    def run_testcase(self, http, testplan):
        if 0 == self.active_status:
            logger.warning('用例[name=%s]处于禁用状态[active=0]，不执行' % self.testcase_name)
            return 'Block'

        protocol_all = http.get_protocol()
        host_all = http.get_host()
        port_all = http.get_port()

        for step in self.steps:
            # 构造测试步骤对象
            step_id = int(step['id'])
            step_number = int(step['step_number'])
            step_action = other_tools.conver_date_from_testlink(step['actions'])
            expected_results = other_tools.conver_date_from_testlink(step['expected_results'])

            logger.debug('step_action： %s' % step_action)

            sql_insert = 'INSERT INTO '+ case_step_report_tb +'(executed_history_id, testcase_id, testcase_name, testplan, project, step_id, step_num, protocol_method, protocol, host, port, ' \
                                                               'step_action, expected_results, runresult, reason, runtime)' \
                         ' VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            data = (executed_history_id, self.testcase_id, self.testcase_name, testplan, self.testproject, step_id, step_number, '', protocol_all, host_all, port_all,
                    step_action, expected_results, 'Block', '', '')

            logger.info('记录测试步骤到测试步骤报告表')
            testdb.execute_insert(sql_insert, data)

            try:
                expected_results = json.loads(expected_results)
                step_action = json.loads(step_action)
                step_obj = CaseStep(step_id, step_number, expected_results, step_action, self.testcase_id)
                protocol_method = step_action['method']
            except Exception as e:
                logger.error('步骤[%s]信息填写错误: %s,停止执行用例[id=%s, name=%s]' % (step_number, e, self.testcase_id, self.testcase_name))
                return 'Error'

            logger.info('开始执行步骤操作[第%s步]'% step_number)
            run_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 记录运行时间
            step_run_result = step_obj.run_step(http)

            if step_run_result[0] == 'Error':
                fail_or_error_reason = step_run_result[1][0][1]
                fail_or_error_reason = fail_or_error_reason.replace('\n', '')
                fail_or_error_reason = fail_or_error_reason.replace('\"', '')
                fail_or_error_reason = fail_or_error_reason.replace('\'', '')
                logger.error('步骤[%s]执行出错,停止执行用例[id=%s, name=%s]' % (step_number, self.testcase_id, self.testcase_name))
                sql_update = 'UPDATE '+ case_step_report_tb +' SET runresult=\"%s\",reason=\"%s\", protocol_method=\"%s\", runtime=\"%s\"' \
                             ' WHERE executed_history_id = %s AND testcase_id = %s AND step_id = %s'\
                             ' AND project=\'%s\' AND testplan=\'%s\'' % \
                              (step_run_result[0], fail_or_error_reason, protocol_method, run_time, str(executed_history_id), self.testcase_id, step_id,
                                 self.testproject, testplan)
                logger.info('正在更新步骤执行结果')
                testdb.execute_update(sql_update)
                return 'Error'
            elif step_run_result[0] == 'Fail':
                fail_or_error_reason = step_run_result[1][0][1]
                fail_or_error_reason = fail_or_error_reason.replace('\n', '')
                fail_or_error_reason = fail_or_error_reason.replace('\"', '')
                fail_or_error_reason = fail_or_error_reason.replace('\'', '')
                logger.info('步骤[%s]执行失败,停止执行用例[id=%s, name=%s]' % (step_number, self.testcase_id, self.testcase_name))
                sql_update = 'UPDATE '+ case_step_report_tb +' SET runresult=\"%s\",reason=\"%s\", protocol_method=\"%s\", runtime=\"%s\"' \
                             ' WHERE executed_history_id = %s AND testcase_id = %s AND step_id = %s'\
                             ' AND project=\'%s\' AND testplan=\'%s\'' % \
                              (step_run_result[0], fail_or_error_reason, protocol_method, run_time, str(executed_history_id), self.testcase_id, step_id,
                                 self.testproject, testplan)
                testdb.execute_update(sql_update)
                return 'Fail'
            else:
                fail_or_error_reason = ''
                sql_update = 'UPDATE '+ case_step_report_tb +' SET runresult=\"%s\",reason=\"%s\", protocol_method=\"%s\", runtime=\"%s\"' \
                             ' WHERE executed_history_id = %s AND testcase_id = %s AND step_id = %s'\
                             ' AND project=\'%s\' AND testplan=\'%s\'' % \
                              (step_run_result[0], fail_or_error_reason, protocol_method, run_time, str(executed_history_id), self.testcase_id, step_id,
                                 self.testproject, testplan)
                logger.info('正在更新步骤执行结果')
                testdb.execute_update(sql_update)

        logger.info('测试用例[id=%s, name=%s]执行成功' % (self.testcase_id, self.testcase_name))
        return 'Pass'

