#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : gwms_menu_page.py
@Author  : liuzhiming
@Time    : 2021/6/16 11:55
"""


from base.base_page import BasePage


class GwmsMenu(BasePage):


    # frame
    frame = "folderForm"
    # “入库处理”--父菜单
    in_storage = ("xpath", ".//*[@id='INSYS']/span")
    in_storage_orders = ("xpath", ".//*[@id='PO_span']")
    in_storage_bill = ("xpath", ".//*[@id='poin_span']")

    # "基础资料"--父菜单
    basic_data = ("xpath", "")
    basic_data_shipper = ("xpath", "")
    incoming_orders = ("xpath", "")
    # “系统管理” -- 父菜单
    system_management = ("xpath", ".//*[@id='SYS']/span")
    shipper_allocation = ("xpath", ".//*[@id='owcoserv']/span[2]")
    shipper_material_allocation = ("xpath", ".//*[@id='owcoIncoSet_span']") # 货主物料配置

    def open_in_storage_orders(self):
        self.swich_to_frame(self.frame)
        self.click(self.in_storage)
        self.click(self.in_storage_orders)

    def open_shipper_material_allocation(self):
        self.swich_to_frame(self.frame)
        self.click(self.system_management)
        self.click(self.shipper_allocation)
        self.click(self.shipper_material_allocation)

