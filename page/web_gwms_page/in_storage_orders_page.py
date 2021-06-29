#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : in_storage_orders_page.py
@Author  : liuzhiming
@Time    : 2021/6/29 11:01
"""

from base.base_page import BasePage
from utils.logger import Logger
import time


class InStoragePage(BasePage):

    """入库处理相关页面操作"""
    logger = Logger().logger
    """
    每个模块的frame都是这个，防止编号变化，每个菜单操作完毕后刷新整个页面
    """
    frame = "tab1_frame"
    ## 入库订单页面，s开头为查询表单，t开头为表单数据中元素
    s_goods_code = ("xpath", ".//*[@id='edit:sk_inna']")    # 商品编码输入框
    s_button = ("xpath", ".//*[@id='edit:sid']")        # 查询按钮

    t_one = ("xpath", ".//*[@id='gtable_table']/tbody/tr[2]/td[5]")
    t_order_bill = ("xpath", ".//*[@id='gtable_biid_1']")       # 第一条数据的入库订单号单元格
    t_source_order = ("xpath", ".//*[@id='gtable_soco_1']")     # 来源单号单元格
    s_submit_button = ("xpath", ".//*[@id='edit:submitMBut']")     # 编辑页面>审核单据按钮
    s_source_order = ("xpath", ".//*[@id='edit:soco']")       # 来源单号输入框


    def audit_order(self, goods_code):
        self.switch_to_frame(self.frame)
        # 输入商品编码进行查询
        self.send_key(self.s_goods_code, goods_code)
        self.click(self.s_button)
        self.sleep(6)

        # 判断第一行记录的入库单号位置的单元格的值
        text = self.get_elem_text(self.t_one)
        print("第一行记录的值为：【{}】".format(text))
        if "_" in text:
            # 获取入库单号、来源单号的值
            self.get_elem_text(self.t_order_bill)
            self.get_elem_text(self.t_source_order)

            # 进入详情进行审核
            self.click(self.t_order_bill)
            self.sleep(3)
            self.click(self.s_submit_button)
            self.sleep(3)
            self.alert_accept()
            self.sleep(3)
            self.alert_accept()
            self.sleep(3)
        else:
            self.logger.error("没有返回数据，请检查此商品是否有对应的入库订单号")










