#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : base_price_sale_parameters.py
@Author  : liuzhiming
@Time    : 2021/11/10 16:22
"""

from base.base_page import BasePage


class PriceParamMaintainPage(BasePage):
    """销售定价参数维护菜单"""
    keyword = ("xpath", "html/body/section/div[3]/section/div[1]/div[1]/div[1]/div[8]/input")     # 关键字查询输入框
    search_btn = ('xpath', "html/body/section/div[3]/section/div[1]/div[1]/div[1]/button")      # 搜索按钮
    detail_btn = ('xpath', "html/body/section/div[3]/section/div[1]/div[2]/div/div[3]/table/tbody/tr/td[11]/div/a[1]/span")    # 第一条记录的详情按钮
    audit_btn = ('xpath', "/html/body/section/div[3]/section/section/div[7]/div")      # 详情页面【提交审核】按钮
    index_url = "http://baseprice.huishoubao.com.cn/salePrice/priceParamMaintain/spuList"     # 定价参数维护url

    def submit_audit(self, product_id):
        """提交审核"""
        self.send_key(self.keyword, product_id)
        self.click(self.search_btn)
        self.click(self.detail_btn)

        if self.find_element(self.audit_btn):
            self.click(self.audit_btn)
            result_message = "机型【{}】已提交审核".format(product_id)
            self.logger.debug(result_message)
            return result_message
        else:
            result_message = "机型【{}】未找到 提交审核 按钮，请检查！".format(product_id)
            self.save_img()
            self.logger.debug(result_message)
            return False


if __name__ == '__main__':
    pass