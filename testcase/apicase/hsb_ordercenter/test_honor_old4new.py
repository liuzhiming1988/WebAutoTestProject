#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : test_honor_old4new.py
@Author  : liuzhiming
@Time    : 2021/8/11 14:41
"""

from apis.honor_data import *
from apis.honor import HonorTestApi
import allure
import pytest
import json


@allure.feature("荣耀保值换新订单服务层")
class TestHonor:

    time13 = times_13()

    data_sync_service = [
        (time13,time13[3:],"1","成功同步服务单","0"),
        (time13,time13[3:],"1","幂等性校验（createTime重复）","tt"),
        (times_13(),time13[3:],"1","幂等性校验（maintainValueServiceOrderId和orderType重复）","0"),
        (times_13(),time13[3:],"2","成功同步退货类型的服务单","0")
    ]

    @allure.story("同步服务单接口测试")
    @allure.title("{case_name}")
    @pytest.mark.demo
    @pytest.mark.parametrize("create_time, service_id, order_type, case_name, expect", data_sync_service)
    def test_sync_services(self, create_time, service_id, order_type, case_name, expect):
        url = "/order_center/old4new/buyHonorMaintainValueService"
        param = buyHonorMaintainValueService()
        param["_param"]["createTime"] = create_time
        param["_param"]["maintainValueServiceList"][0]["maintainValueServiceOrderId"] = service_id
        param["_param"]["orderType"] = order_type
        res = HonorTestApi()._post(url, param)
        res = json.loads(res)
        err_code = res["_data"]["_errCode"]
        pytest.assume(err_code == expect), "errCode为0表示业务请求成功，无异常！"
        print("测试完成测试完成测试完成测试完成测试完成测试完成测试完成测试完成测试完成测试完成测试完成")






