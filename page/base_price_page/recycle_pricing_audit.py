#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : recycle_pricing_audit.py
@Author  : liuzhiming
@Time    : 2021/11/12 9:40
"""

from base.base_page import BasePage


class RecyclePricingAuditPage(BasePage):
    """回收定价审核菜单"""
    search_type = ("xpath", "/html/body/section/div[3]/section/div[2]/div[5]/div[1]/input")     # 名称/ID搜索框
    id_search = ("xpath", "/html/body/div/div[1]/div[1]/ul/li[2]/span")     # ID搜索
    search_input = ("xpath", "/html/body/section/div[3]/section/div[2]/div[6]/input")     # 关键字输入框
    search_btn = ("xpath", "/html/body/section/div[3]/section/div[2]/button")     # 搜索按钮
    audit_btn = ("xpath", "/html/body/section/div[3]/section/div[3]/div/div[3]/table/tbody/tr/td[9]/div/div[1]/a/span")    # 审核按钮
    pass_audit_btn = ("xpath", "/html/body/section/div[3]/section/div[5]/div/div[2]/div/div/div[7]/div[3]")      # 审核通过按钮
    sure_btn = ("xpath", "/html/body/div[2]/div/div[3]/button[2]/span")     # 确认按钮

    def pass_audit(self, product_id):
        """审核通过菜单"""
        self.click(self.search_type)
        self.click(self.id_search)
        self.send_key(self.search_input, product_id)
        self.click(self.search_btn)

        if self.find_element(self.audit_btn):
            self.click(self.audit_btn)
            self.click(self.pass_audit_btn)
            self.click(self.sure_btn)
            result_message = "机型【{}】已通过审核".format(product_id)
            self.logger.debug(result_message)
            return result_message
        else:
            result_message = "机型【{}】未找到 待审核 记录，请检查！".format(product_id)
            self.save_img()
            self.logger.debug(result_message)
            return result_message


if __name__ == '__main__':
    pass