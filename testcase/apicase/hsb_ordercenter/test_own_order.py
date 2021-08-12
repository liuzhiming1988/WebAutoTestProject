#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : test_own_order.py
@Author  : liuzhiming
@Time    : 2021/6/4 9:54
"""

import allure
import pytest
from apis.hsb_app_api import HsbAppApi


@allure.feature("【回收宝APP】订单服务测试")
class TestOwnOrder:

    data = [
        ("38200", "success", "机型iPhone8，下单成功"),
        ("64001", "success", "机型华为P40 pro，下单成功"),
        ("62790", "success", "荣耀20，下单成功"),
        ("59939", "success", "小米9，下单成功")
    ]

    @allure.story("【回收宝app】邮寄回收单用例")
    @allure.title("{case_name}")
    @pytest.mark.demo
    @pytest.mark.parametrize("product_id, expect, case_name", data)
    @pytest.mark.flaky(reruns=2, reruns_delay=5)    # 用例失败时重新运行2次，间隔5秒钟
    def test_place_order(self, product_id, expect, case_name):
        # 所有机型的id列表
        # 校验登录成功或失败
        """回收宝APP，邮寄回收-下单测试用例"""
        own = HsbAppApi()
        own.login()
        own.get_balance_info()
        own.get_procduct_list()
        own.extract_product()
        if own.mark:
            own.get_service_time()
            own.get_address()
            own.get_store_list()
            own.get_product_param(product_id)
            own.get_select()
            own.get_evaluate(product_id)
            own.get_allow_coupon_list(product_id,5)
            own.get_price_history(product_id)
            own.get_evaluate_result()
            own.place_order_sending()
        check_text = own.mark_text
        assert "下单成功" in check_text


if __name__ == '__main__':
    pytest.main(["-v", "-s", "test_own_order.py"])
    # OwnOrderT().place_order()