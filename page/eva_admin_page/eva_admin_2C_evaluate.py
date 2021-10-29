#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : eva_admin_2C_evaluate.py
@Author  : liuzhiming
@Time    : 2021/10/20 18:59
"""

from base.base_page import BasePage
from config.config_read import ConfigRead
from utils.common import *
import allure
from utils.ding_rebot import DingRebot


class Eva2cPage(BasePage):
    """2.0估价系统菜单处理页面"""
    keyword = ("xpath", ".//*[@id='toC']/div/div/div/div[2]/div[3]/div/input")     # 关键字查询输入框
    search_btn = ('xpath', ".//*[@id='toC']/div/div/div/div[2]/span[2]/button")      # 搜索按钮
    oper_btn = ('xpath', ".//*[@id='toC']/div/div/div/div[3]/table/tr[2]/td[7]/button")    # 第一条记录的操作按钮
    bottom_btn = ('xpath', ".//*[@id='toC']/div/div[2]/div/div[2]/div/div[2]")      # 详情页面【底部】按钮
    return_btn = ("xpath", ".//*[@id='toC']/div/div[2]/div/div[2]/div/div[3]")        # 返回按钮
    save_btn = ("xpath", ".//*[@id='toC']/div/div[2]/div/div[1]/div[22]/button[2]")     # 详情页面【保存】按钮
    save_title = ("xpath", "/html/body/div[2]/p")         # 保存成功后的提示
    close_message = ("xpath", "/html/body/div[2]/i[2]")     # 关闭提示

    # ding_rebot = DingRebot()

    def save_product(self, product_id):
        self.send_key(self.keyword, product_id)
        self.click(self.search_btn)
        self.sleep(1)
        self.click(self.oper_btn)
        self.sleep(5)
        self.click(self.bottom_btn)
        self.click(self.save_btn)
        self.sleep(8)
        if self.find_element(self.save_title):
            result_message = "机型【{}】保存成功".format(product_id)
            # self.ding_rebot.send_text(result_message)
            self.logger.info(result_message)
            self.sleep(3)
            self.click(self.close_message)
            self.click(self.return_btn)
        else:
            result_message = "机型【{}】结果未知，请手动检查或重试！".format(product_id)
        return result_message


if __name__ == '__main__':
    # copy和deepcopy
    import copy
    a = [1,2,[3,4,5],6,7]
    b = copy.copy(a)
    c = copy.deepcopy(a)
    a.append(8)
    a[2].append(9)
    b.append("88")
    b[2].append("66")

    print("a=", a)
    print("b=", b)
    print("c=", c)


