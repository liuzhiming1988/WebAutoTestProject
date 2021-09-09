#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : outbound_page.py
@Author  : liuzhiming
@Time    : 2021/9/1 19:43
"""


# 每个模块的frame都是这个，防止编号变化，每个菜单操作完毕后刷新整个页面
frame = "tab1_frame"

frame_index = "list_iframe"

# 销售订单定位对象
more_query = ("xpath", ".//*[@id='detail_ctrl']")     # 展开更多查询条件
order_statu_query = ("xpath", ".//*[@id='multi_select']/input[1]")    # 订单状态查询条件
order_statu_query_all = ("xpath", ".//*[@id='multi_select']/div[1]/div[1]/input[1]")    # 订单状态查询条件
code_input = ("xpath", ".//*[@id='edit:sk_inco']")     # 商品编码查询条件输入框
query_btn = ("xpath", ".//*[@id='edit:sid']")     # 查询按钮
stock_status = ("xpath", ".//*[@id='gtable_isck_1']")     # 库存状态
order_status = ("xpath", ".//*[@id='gtable_flag_1']")     # 单据状态
tracking_number = ("xpath", ".//*[@id='gtable_lpid_1']")     # 快递单号
create_task = ("xpath", ".//*[@id='edit:createOutTask_h']")     # 手动生成任务
picking_list = ("xpath", ".//*[@id='gtable_pkbiid_1']")     # 备货任务单
label = ("xpath", ".//*[@id='gtable_inty_1']")     # 是否一单多货标记
sale_order = ("xpath", ".//*[@id='gtable_biid_1']")     # 销售订单号

# 拣货下架定位对象
add_btn = ("xpath", ".//*[@id='edit:j_id_jsp_1442365406_2']")     # 添加单据按钮
source_number_input = ("xpath", ".//*[@id='edit:soco']")     # 添加拣货下架单：来源单号输入框
save_btn = ("xpath", ".//*[@id='edit:addId']")     # 添加拣货下架单：保存按钮
pick_task_quick = ("xpath", ".//*[@id='detail_ctrl']")     # 展开拣货下架任务明细
quick_pick_btn = ("xpath", ".//*[@id='edit:addDBut']")     # 快捷拣货按钮
check_all = ("xpath", ".//*[@id='gtable1_checkboxall']")     # 全选按钮
save_order_btn = ("xpath", ".//*[@id='edit:updateId']")     # 保存单据按钮
audit_order_btn = ("xpath", ".//*[@id='edit:submitMBut']")     # 审核单据按钮

# 出库复核定位对象
review_add_btn = ("xpath", ".//*[@id='edit:j_id_jsp_1417180024_2']")     # 出库复核-添加单据按钮
radio_code = ("xpath", ".//*[@id='edit:batp:2']")     # 明细复核，商品编码单选框
review_code = ".//*[@id='gtable2_inco_1']"     # 第一条明细的商品编码
review_code_num = ".//*[@id='gtable2_tanu_1']"   # 第一条明细的数量
review_code_input = ("xpath", ".//*[@id='edit:baco']")     # 条码输入框
code_count = ("xpath", ".//*[@id='edit:qty']")     # 数量输入框
record_count = ("xpath", ".//*[@id='gtable2_stotalRecords']")    # 待复核明细记录数
review_save_btn = ("xpath", ".//*[@id='edit:updateId']")    # 复核-保存单据按钮
review_audit_btn = ("xpath", ".//*[@id='edit:appBut']")    # 复核-审核单据按钮


from base.base_page import BasePage
from utils.logger import Logger
import random


class OutboundPage(BasePage):
    """出库处理相关页面操作"""
    logger = Logger().logger
    order_label = ""
    sale_order_num = ""
    task_order = ""
    mark_text = ""
    mark = True

    def create_express_number(self):
        """生成快递单号"""

        pass

    def import_express_number(self):
        """导入快递单号"""
        pass

    def create_task(self, p_code):
        self.switch_to_frame(frame)
        # self.max_window()
        # 用商品编码搜索出对应的订单
        self.click(more_query)
        self.send_key(code_input, p_code)
        self.click(order_statu_query)   # 查询所有状态
        self.click(order_statu_query_all)
        self.click(query_btn)
        self.sleep(5)

        self.switch_to_frame(frame_index)

        # 判断第一行记录的销售订单号，并判断是否存在
        sale_ob = self.get_elem_text(("xpath", ".//*[@id='gtable_table']/tbody/tr[2]/td[20]"))
        if sale_ob == " ":
            self.mark_text = "搜索不到对应的销售订单，无法出库！"
            self.logger.info(self.mark_text)
            return False
        else:
            self.sale_order_num = self.get_elem_text(sale_order)
            self.logger.info("已找到销售订单：{}".format(self.sale_order_num))

        # 判断库存状态是否是已锁库存
        if self.get_elem_text(stock_status) == "已锁库存":
            pass
        else:
            self.mark_text = "当前库存状态为【{}】，无法进行出库！<br>" \
                             "tip：库存状态需为已锁库存，才可以进行出库，建议检查当前单据包含的条码是否都已入库完成！"
            return False

        # 获取是否单品
        self.order_label = self.get_elem_text(label)

        # 获取订单状态，正式单据状态pass
        self.order_label = self.get_elem_text(label)
        status = self.get_elem_text(order_status)
        if status == "正式单据":
            pass
        else:
            self.mark_text = "当前订单状态为：{}；订单状态需为【正式单据】，才可以进行出库，请检查！！！".format(status)
            return False

        # 获取物流单号
        express_num = self.get_elem_text(tracking_number)

        # 判断是否有物流单号，没有则调用导入订单号方法，若有则跳过
        if express_num:
            pass
        else:
            self.import_express_number()

        # 生成任务单
        self.click(("xpath", ".//*[@id='gtable_checkbox1']"))  # 选中
        self.switch_to_parent_frame()
        self.click(create_task)
        self.mark = True

        # 获取备货任务单
        self.switch_to_frame(frame_index)
        self.task_order = self.get_elem_text(picking_list)

        # 再次获取物流单号
        express_num = self.get_elem_text(tracking_number)

        text = "1. 【商品编码】{}，【对应订单号】{}，【物流单号】{}，【单据类型】{}，备货任务生成成功;【备货单号】{}<br>".format(
            p_code, self.sale_order_num, express_num, self.order_label, self.task_order)
        self.logger.debug(text)
        self.mark_text = text
        self.refresh()

    def picking_off(self):
        self.switch_to_frame(frame)
        # 添加单据
        self.click(add_btn)
        self.send_key(source_number_input, self.task_order)
        self.click(save_btn)
        self.alert_accept()

        # 快捷拣货
        self.click(pick_task_quick)
        self.click(check_all)
        self.click(quick_pick_btn)
        self.alert_accept()

        # 保存、审核单据
        self.click(save_order_btn)
        self.alert_accept()
        self.click(audit_order_btn)
        self.alert_accept()

        text = "2. 【备货单号】{}拣货完成<br>".format(self.task_order)
        self.logger.debug(text)
        self.mark_text += text

        self.refresh()

    def outbound_review(self):
        self.switch_to_frame(frame)

        # 添加出库复核单据
        self.click(review_add_btn)
        self.send_key(source_number_input, self.sale_order_num)
        self.click(save_btn)
        self.alert_accept()

        # 获取待复核的明细记录数，调用create_detail_element()方法生成明细对象
        # 商品编码xpath：".//*[@id='gtable2_inco_1']"     待复核数量xpath：".//*[@id='gtable2_tanu_1']"
        count = int(self.get_elem_text(record_count))
        code_list = self.create_detail_element(review_code, count)
        num_list = self.create_detail_element(review_code_num, count)
        self.click(radio_code)  # 明细类型选择商品编码

        for x in range(count):
            # 遍历明细，循环添加明细
            code = self.get_elem_text(code_list)
            num = self.get_elem_text(num_list)
            self.send_key(review_code_input, code)
            self.send_key(review_code_num, num)

        # 保存单据、审核单据
        self.click(review_save_btn)
        self.alert_accept()
        self.click(review_audit_btn)
        self.alert_accept()

        text = "3. 【销售单号】{}出库完成".format(self.sale_order_num)
        self.logger.debug(text)
        self.mark_text += text
        self.refresh()



    @staticmethod
    def create_detail_element(element_name, count, index=-3):
        """
        生成多个元素定位对象，以列表形式返回
        :param element_name: 元素前缀
        :param count: 数量
        :param index: 要替换的序号位置，默认为-3
        :return: 元素定位对象列表，类似[('xpath', 'test1'), ('xpath', 'test2'), ('xpath', 'test3')]
        """
        object_list = []
        if isinstance(count, str):
            count = int(count)
        for i in range(1, count+1):
            str_list = list(element_name)
            str_list[index] = str(i)
            ele_final = "".join(str_list)
            ob = ("xpath", ele_final)
            object_list.append(ob)
        return object_list


if __name__ == '__main__':
    a = ["a1", "a2", "a3", "a4"]  # 单选
    b = ["b1", "b2", "b3", "b4"]  # 单选
    c = ["c1", "c2", "c3", "c4"]  # 第一个值为单选，其它可多选
    d = ["d1", "d2", "d3"]    # 多选
    # 从a、b、c、d里边挑选值进行排列组合，多选项以列表形式进行排列，如["a1","b2",[c2,c3],[d1,d2,d3]]
    # 业务：有34个问题项，每个问题项对应若干答案，答案可能为单选或多选，将所有答案输出为一个列表，
    # 作为参数去请求接口进行估价，验证估价算法是否正确。
    def temp():
        # finnal_list = []
        count = 0
        for x in a:
            res_list = [1, 2, 3, 4]
            res_list[0] = x
            for y in b:
                res_list[1] = y
                for z in c:
                    res_list[2] = z
                    for s in d:
                        res_list[3] = s
                        print(res_list)
                        count += 1
        print(count)

    temp()

    # pass










