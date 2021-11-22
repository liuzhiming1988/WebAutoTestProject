#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : shipper_allocation_page.py
@Author  : liuzhiming
@Time    : 2021/6/28 18:02
"""

from base.base_page import BasePage
import time


class ShipperAllocationPage(BasePage):

    # 货主物料配置页面
    frame = "tab1_frame"
    newButton = ("xpath", ".//*[@id='list:saveButton']")   # 新增按钮
    controlCode = ("xpath", ".//*[@id='edit:cotl']")     # 管控编码
    productCode = ("xpath", ".//*[@id='edit:inco']")     # 商品编码
    codeType = ("xpath", ".//*[@id='edit:boty']/option")       # 码制类型
    batchManage = ("xpath", ".//*[@id='edit:baty']/option")     # 批次管理方式
    saveButton = ("xpath", ".//*[@id='edit:saveid']")     # 保存按钮
    message = ("xpath", ".//*[@id='message_alert_id']/table/tbody/tr/td[2]/span")     # 系统提示
    alertConfirmButton = ("xpath", ".//*[@id='button_alert_id']/input")     # 弹窗中的确定按钮

    def switch_frame(self):
        self.switch_to_frame(self.frame)

    def click_new_button(self):
        self.click(self.newButton)

    def set_control_code(self, value):
        self.send_key(self.controlCode, value)

    def set_product_code(self, value):
        self.send_key(self.productCode, value)

    def set_code_type(self, num):
        elem = self.find_elements(self.codeType)
        elem[num].click()

    def set_batch_manage(self, num):
        elem = self.find_elements(self.batchManage)
        elem[num].click()

    def click_save_button(self):
        self.click(self.saveButton)

    def show_message(self):
        text = self.find_element(self.message).text
        self.logger.info(text)
        self.click(self.alertConfirmButton)

    def add_material_code(self):

        self.switch_frame()
        self.click_new_button()
        self.set_control_code("01")
        self.set_product_code("all")
        self.set_code_type(2)
        self.set_batch_manage(4)
        self.click_save_button()
        self.show_message()
        self.refresh()
        self.sleep(3)






