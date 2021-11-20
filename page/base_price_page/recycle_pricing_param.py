#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : recycle_pricing_param.py
@Author  : liuzhiming
@Time    : 2021/11/12 9:40
"""

from base.base_page import BasePage


class RecyclePriceParamPage(BasePage):
    """销售定价参数维护菜单"""
    keyword = ("xpath", "/html/body/section/div[3]/section/div/div[2]/div[1]/div[5]/input", "关键字查询输入框")     # 关键字查询输入框
    search_btn = ('xpath', "/html/body/section/div[3]/section/div/div[2]/div[1]/button", "列表-搜索按钮")      # 搜索按钮
    detail_btn = ('xpath', "/html/body/section/div[3]/section/div/div[3]/div/div[3]/table/tbody/tr/td[9]/div/a[1]/span", "首条记录-详情按钮")    # 第一条记录的详情按钮
    audit_btn = ('xpath', "/html/body/section/div[3]/section/section/div[7]/div", "提交审核按钮")      # 详情页面【提交审核】按钮
    message = ("xpath", "/html/body/div[1]/div/div[2]/div[1]/div/p", "提示语")      # 提示语

    def submit_audit(self, product_id):
        """提交审核"""
        self.send_key(self.keyword, product_id)
        self.click(self.search_btn)
        if self.find_element(self.detail_btn):
            self.click(self.detail_btn)
            self.scroll_to(x=0, y=100)
            self.sleep(3)
            self.click(self.audit_btn)
            result_message = "机型【{}】已提交成功".format(product_id)
            self.logger.debug(result_message)
            return result_message
        else:
            result_message = "机型【{}】未查找到记录，请检查！".format(product_id)
            self.save_img()
            self.logger.debug(result_message)
            return False


if __name__ == '__main__':
    pass