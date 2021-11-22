#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : menu_page.py
@Author  : liuzhiming
@Time    : 2021/6/16 11:55
"""


from base.base_page import BasePage
from utils.logger import Logger
from utils.ding_rebot import DingRebot
import traceback


# 写一个装饰器，打开父模块以及最后跳出frame,装饰器修饰类并调用类中的方法
def swi_frame(func):
    def wrapper(self, *args, **kwargs):
        self.switch_to_frame(self.frame)
        res = func(self, *args, **kwargs)
        self.switch_to_default_frame()
        return func
    return wrapper


class GwmsMenuPage(BasePage):

    # frame
    frame = "folderForm"

    # “入库处理”--父菜单
    in_storage = ("xpath", ".//*[@id='INSYS']/span")   # 入库处理
    in_storage_orders = ("xpath", ".//*[@id='PO_span']")   # 入库订单
    arrival_list = ("xpath", ".//*[@id='ARRIVE_span']")    # 到货清单
    in_storage_bill = ("xpath", ".//*[@id='poin_span']")   # 入库单

    # 出库处理
    outbound_index = ("xpath", ".//*[@id='OUTSYS']/span")    # 出库主菜单
    order_menu = ("xpath", ".//*[@id='ORDERDEAL']/span[2]")      # 订单子菜单
    sale_order_menu = ("xpath", ".//*[@id='OUTORDER_span']")    # 销售订单子菜单
    picking_menu = ("xpath", ".//*[@id='PICKDWDEAL']/span[2]")     # 拣货
    pick_down_menu = ("xpath", ".//*[@id='PICKDOWN_span']")    # 拣货下架
    review_menu = ("xpath", ".//*[@id='OQCDEAL']/span[2]")      # 复核
    outbound_review_menu = ("xpath", ".//*[@id='oqc_span']")     # 出库复核


    # "基础资料"--父菜单
    basic_data = ("xpath", "")   # 基础资料
    basic_data_shipper = ("xpath", "")
    incoming_orders = ("xpath", "")

    # “系统管理” -- 父菜单
    system_management = ("xpath", ".//*[@id='SYS']/span")   # 系统管理
    shipper_allocation = ("xpath", ".//*[@id='owcoserv']/span[2]")     # 货主配置
    shipper_material_allocation = ("xpath", ".//*[@id='owcoIncoSet_span']")   # 货主物料配置

    # 定义进入各个菜单的方法，跳入frame>进入菜单>返回默认frame，方便后续操作
    @swi_frame
    def open_in_storage_orders(self):
        """open the in_storage_orders menu"""
        self.click(self.in_storage)
        self.click(self.in_storage_orders)

    @swi_frame
    def open_storage_order(self):
        """open the storage_order"""
        self.click(self.in_storage)
        self.click(self.in_storage_bill)

    @swi_frame
    def open_shipper_material_allocation(self):
        """
        打开货主物料配置菜单
        """
        self.click(self.system_management)
        self.click(self.shipper_allocation)
        self.click(self.shipper_material_allocation)

    @swi_frame
    def open_sale_order(self):
        """
        打开出库处理->订单->销售订单菜单
        """
        self.click(self.outbound_index)
        self.click(self.order_menu)
        self.click(self.sale_order_menu)

    @swi_frame
    def open_picking(self):
        """
        打开出库处理->拣货->拣货下架
        """
        self.click(self.outbound_index)
        self.click(self.picking_menu)
        self.click(self.pick_down_menu)

    @swi_frame
    def open_outbound_review(self):
        """
        打开出库处理->复核->出库复核菜单
        """
        self.click(self.outbound_index)
        self.click(self.review_menu)
        self.click(self.outbound_review_menu)

