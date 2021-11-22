#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : outbound.py
@Author  : liuzhiming
@Time    : 2021/9/2 19:37
"""
from page.web_gwms_page import login_page
from page.web_gwms_page import menu_page
from page.web_gwms_page import outbound_page
from utils.logger import LoggerV2
from selenium import webdriver


class TestOutbound:

    def test_outbound(self, product_code):
        """

        :param product_code: 商品编码
        :return:
        """
        text = ""    # 接收执行结果
        logger = LoggerV2()
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        get_driver = webdriver.Chrome(options=options)

        login = login_page.GwmsLoginPage(get_driver)
        menu = menu_page.GwmsMenuPage(get_driver)
        outbound = outbound_page.OutboundPage(get_driver)

        login.login()

        # 出库处理
        try:
            menu.open_sale_order()
            outbound.create_task(product_code)

            if outbound.mark:
                menu.open_picking()
                outbound.picking_off()
            if outbound.mark:
                menu.open_outbound_review()
                outbound.outbound_review()

            logger.info(outbound.mark_text)
            return outbound.mark_text

        except Exception as e:
            text = outbound.mark_text+"出库失败，请登录系统检查日志信息"
            return text
        finally:
            logger.info("{}测试完成".format(product_code))
            get_driver.quit()


if __name__ == '__main__':
    # out = TestOutbound()
    # out.test_outbound("SJ5990003883073390")
    # out.test_outbound("SJ6840004239524585")
    kv = {"A":"a","B":"b"}
    for k,v in kv.items():
        print(k+"="+v)
