#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : new_standard_detect.py
@Author  : liuzhiming
@Time    : 2021/7/14 16:40
"""

from apis.detection_admin import DetectionClient
from flask import Blueprint
from flask import Flask
from flask import request
import json
from flask import render_template

detect_blue = Blueprint("new_standard_detect", __name__)


@detect_blue.route("/new_standard_detect", methods=['GET', 'POST'])
def new_standard_detect():
    text = ""
    if request.method == "POST":
        detect_code_raw = request.form.get("detect_code_list")
        detect_code_list = detect_code_raw.strip()
        detect_code_list = detect_code_list.split(",")
        detection = DetectionClient()
        detection.get_auth()
        for detect_code in detect_code_list:
            text += "检测条码：【{}】<br />".format(detect_code)
            if len(detect_code) == 18:
                detect_result_raw = json.loads(detection.get_detect_info(detect_code))
                detect_code_result = detect_result_raw["raw_data"]["_data"]["_errStr"]
                if detect_code_result == "success":
                    detection.search_product()
                    detection.get_detect_option()
                    # 获取检测选项
                    options = detection.temp["options"]
                    # 获取选中的选项
                    options_select = detection.get_options_select(options)
                    engineer_options = options_select[0]
                    # 获取选中的id列表
                    select_ids = options_select[1]
                    # 获取选中的sku列表，七项
                    sku_list = detection.get_sku_list(select_ids)
                    detection.get_sku_id(sku_list)
                    detection.get_product_evaluate(engineer_options, sku_list)
                    detection.get_level(select_ids)
                    # print(detection.temp["level"])
                    product_info = detection.temp["product_info"]
                    product_id = detection.temp["productId"]
                    for product in product_info:
                        for i in range(len(product_info)):
                            fproduct = product_info[i]
                            fproduct_id = fproduct["fproduct_id"]
                            if fproduct_id == product_id:
                                detection.temp = dict(detection.temp, **fproduct)
                                break
                            else:
                                pass
                    detection.get_warehouse_type(select_ids)
                    detIds = []
                    detectEvaluateOptionIds = detection.temp["detectEvaluateOptionIds"]
                    for id_ in detectEvaluateOptionIds:
                        dict_temp = {
                            "id": id_,
                            "mp": []
                        }
                        detIds.append(dict_temp)

                    detection.logger.info(json.dumps(detection.temp, indent=6))
                    detect_result = json.loads(detection.add_detect_info(
                        detIds, engineer_options, select_ids, sku_list))
                    detect_mark_text = detect_result["raw_data"]["_data"]["_errStr"]

                    if detect_mark_text == "检测成功":
                        clear_result = json.loads(detection.clear_option())
                        clear_mark_text = clear_result["raw_data"]["_data"]["_errStr"]
                        text += "检测结果：{}；<br />".format(detect_mark_text)
                        text += "清除结果：{} <br /> <hr />".format(clear_mark_text)
                    else:
                        text += "检测结果：{}；<br /> <hr />".format(detect_mark_text)
                else:
                    text += detect_code_result+"<br /><hr />"
            else:
                text += "条码输入错误，请输入正确的数据，不能为空！<br /><hr />"
    # return text
    return render_template("tips.html", text=text)
