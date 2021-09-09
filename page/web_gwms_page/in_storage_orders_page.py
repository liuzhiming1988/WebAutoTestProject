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

    ## 入库单元素
    addBillBtn = ("id", "edit:j_id_jsp_107150791_2")      # 添加单据按钮
    sourceOrdSearchImg= ("id", "orid_img")                        # 来源单号搜索图标
    frameSearchSource = "iframe_Gwin_selectTask42"            # 来源单号搜索弹窗
    sourceInput = ("id", "edit:soco_po")              # 来源单号搜索框
    selectBtn = ("id", "edit:sid")            # 查询按钮
    saveBillBtn = ("id", "edit:updateId")       # 保存单据按钮
    auditBtn = ("id", "edit:submitMBut")        # 审核单据按钮
    firstSourceOrder = ("id", "gtable_rowid_1")    # 列表中第一条数据
    saveBtn = ("id", "edit:addId")      # 保存按钮
    addDetailBtn = ("id", "edit:addDBut")     # 添加明细按钮
    barCodeSearch = ("id", "inty_img_baco")      # 条码搜索
    frameBarCode = "iframe_Gwin_inve59"     # 条码搜索弹出框frame
    firstBarCode = ("id", "gtable_rowid_1")     # 第一条条码记录
    qtyInput = ("id", "edit:qty")      # 数量输入框
    dwhidInput = ("id", "edit:dwhid")# 库位输入框，第一个值是01A01-A-01-01

    def audit_order(self, barCode):
        time_ = 5
        self.switch_to_frame(self.frame)
        # 输入商品编码进行查询
        self.send_key(self.s_goods_code, barCode)
        self.click(self.s_button)
        self.sleep(time_)

        # 判断第一行记录的入库单号位置的单元格的值
        text = self.get_elem_text(self.t_one)
        print("第一行记录的值为：【{}】".format(text))
        if "_" in text:
            # 获取入库单号、来源单号的值
            self.get_elem_text(self.t_order_bill)
            source_order = self.get_elem_text(self.t_source_order)

            # 进入详情进行审核
            self.click(self.t_order_bill)
            self.sleep(time_)
            self.click(self.s_submit_button)
            self.alert_accept()
            self.alert_accept()

            self.refresh()
            self.sleep(time_)
            return source_order
        else:
            self.logger.error("没有返回数据，请检查此商品是否有对应的入库订单号")
            return False

    def add_storage_order(self, source_order):
        time_ = 5
        self.switch_to_frame(self.frame)
        self.click(self.addBillBtn)  # 点击添加单据按钮
        self.click(self.sourceOrdSearchImg)      # 点击来源单号搜索
        self.sleep(time_)
        self.switch_to_frame(self.frameSearchSource)
        self.send_key(self.sourceInput, source_order)
        self.click(self.selectBtn)
        self.sleep(time_)
        self.click(self.firstSourceOrder)    # 选中第一条查询结果
        self.sleep(time_)
        self.switch_to_frame(self.frame)
        self.click(self.saveBtn)
        self.alert_accept()
        self.click(self.barCodeSearch)
        self.sleep(time_)
        self.switch_to_frame(self.frameBarCode)
        self.click(self.firstBarCode)
        self.sleep(time_)
        self.switch_to_frame(self.frame)
        self.send_key(self.qtyInput, "1")
        self.send_key(self.dwhidInput, "01A01-A-01-01")
        self.click(self.addDetailBtn)
        self.sleep(time_)
        self.sleep(time_)
        self.click(self.saveBillBtn)
        self.logger.info("保存单据成功")
        self.alert_accept()
        self.sleep(time_)
        self.logger.info("点击审核单据")
        self.click(self.auditBtn)
        self.alert_accept()
        text = "3. 恭喜你！！！入库成功！！！"
        return text

    def test_button(self):
        self.switch_to_frame(self.frame)
        first = ("id", "gtable_biid_1")
        self.click(first)
        self.sleep(5)
        self.click(self.saveBillBtn)
        self.sleep(20)

