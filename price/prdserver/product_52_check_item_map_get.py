#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 52 获取标准检测选项映射的估价选项 - http://wiki.huishoubao.com/web/#/105?page_id=15643
    1. 对应服务：server-evaluate_detect（服务器应用名：server-evaluate_detect）
    2. 对应URL http://codserver.huishoubao.com

    入参：checkAnsId：标准检测答案项列表
    出参：mapList：映射列表  |  checkAnsId：标准检测答案项  |  itemMap：映射信息  |  queId：估价问题项Id
        queName：估价问题项名称  |  ansId：估价答案项Id  |  ansName：估价答案项名称
'''

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test, hsb_response_print

class Check_Item_Map_Get:
    def __init__(self):
        self.secret_key = "gYt8YHmZVUtq9BxHzmNBQ0Eo7oGi8IKU"
        self.callerserviceid = "112006"

    def product_check_item_57(self, productId):
        param = {"_head": {"_interface": "product_check_item", "_msgType": "request", "_remark": "", "_version": "0.01","_timestamps": "123456", "_invokeId": "test_zhangjinfa", "_callerServiceId": "112006","_groupNo": "1"}, "_param": {"productId": productId}}
        url = "http://codserver.huishoubao.com/detect/product_check_item"
        md5value = json.dumps(param) + "_" + self.secret_key
        headers = {"Content-Type": "application/json;charset=UTF-8", "HSB-OPENAPI-SIGNATURE": Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID": self.callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置
        respone_dict = json.loads(respone.text)  # 转成字典
        checkList = respone_dict['_data']['_data']['checkList']
        skuList = respone_dict['_data']['_data']['skuList']

        strCheckList = []
        strCheckDesc = ''
        for info in checkList:
            answerList = info['answerList']
            index = random.randint(0, len(answerList) - 1)
            strCheckList.append(answerList[index]['answerId'])
            strCheckDesc += '"' + info['questionName'] + ":" + answerList[index]['answerName'] + '",'

        return strCheckList, strCheckDesc

    def check_item_map_get(self, productId):
        # (strCheckList, strCheckDesc) = self.product_check_item_57(productId=productId)

        # strCheckList = '' #"_errStr":"checkAnsId 参数错误"
        strCheckList = [] #检测vector选项为空
        # strCheckList = ['7420', '7422', '7426'] #部分机况
        # strCheckList = ['7420', '7423', '7425', '7429', '7432', '7440', '7443', '7446', '7450', '7453', '7460', '7462', '7466', '7467', '7472', '7476', '7483', '7487', '7492', '7494', '7504', '7506', '7510', '7520', '7522', '7615', '7533', '7537', '7544', '7548', '7555', '7556', '7559', '7563', '7571', '7574', '7578', '7581', '7588', '7589', '7599', '7613'] #完整机况
        # strCheckList = ['7429', '7430'] #某个机况传了多个选项
        # strCheckList = ['7420', '7422', '7426','12'] #机况+SKU（12） -- 正常当机况选项去查，能查到返回，查不到不返回
        # strCheckList = ['7420', '7422', '7426','20210717'] #机况+任意数字
        # strCheckList = ['aaaa', 12345,'20210717'] #"_errStr":"checkAnsId 参数错误, 必须是数字"
        # strCheckList = ['44444', 12345,'20210717'] #"_errStr":"checkAnsId 参数错误, 必须是数字"
        # strCheckList = ['44444', '12345','20210717'] # 正常查，查不到，返回为空  "_data":{"mapList":[]}

        param = {"_head":{"_interface":"check_item_map_get","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"123456","_invokeId":"123456","_callerServiceId":"112006","_groupNo":"1"},"_param":{"checkAnsId":strCheckList}}
        url = "http://codserver.huishoubao.com/detect/check_item_map"
        md5value = json.dumps(param) + "_" + self.secret_key
        headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":self.callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置

        # print('\n========>3.『{0}』 产品的『检测标准化选项-机况-34』(随机取)为：\n'.format(productId), strCheckList)
        # print('\n========>4. 以上『检测标准化选项-机况-34』为：\n', '{' + strCheckDesc[:-1] + '}')
        hsb_response_print(respone=respone)

if __name__ == '__main__':
    p52 = Check_Item_Map_Get()
    # p52.check_item_map_get(checkAnsId='') #"_errStr":"checkAnsId 参数错误"
    # p52.check_item_map_get(checkAnsId=[]) #检测vector选项为空
    p52.check_item_map_get(productId='41567') #检测vector选项为空


'''
测试
SELECT Fanswer_id, Feva_id, Fweight FROM t_check_mapping_eva, t_eva_item_base WHERE t_eva_item_base.Fid = t_check_mapping_eva.Feva_id AND t_check_mapping_eva.Fvalid = 1 AND t_eva_item_base.Fvalid = 1 AND t_check_mapping_eva.Fanswer_id IN (7420,7422,7426,7430,7434,7438,7442,7446,8055,7452,7460,7463,7465,7469,7470,7479,7483,7487,7490,7497,7502,7508,7510,7519,7523,7530,7532,7536,7545,7547,7553,7557,7559,7563,7570,7574,7578,7580,7588,7589,7600,7613)

select t_a.Fid as Faid, t_a.Fname as Faname, t_q.Fid as Fqid, t_q.Fname as Fqname  from t_eva_item_base as t_a, t_eva_item_base as t_q  where t_a.Fpid=t_q.Fid and t_a.Flevel=3 and t_q.Flevel=2 and t_a.Fid in (24,7420,20,7422,8,82,7426,79,7430,79,7434,7438,77,2168,7442,2167,5530,7446,73,2167,7452,71,3248,7460,68,7463,68,7465,69,7469,71,3248,7470,2165,3247,7479,3245,7483,63,7487,63,7490,7642,224,223,223,79,56,56,77,65,65,65,63,62,63,7642,63,63,63,63,53,1078,2170,59,3244)
'''