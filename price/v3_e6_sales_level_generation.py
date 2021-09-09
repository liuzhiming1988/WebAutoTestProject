#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 估价服务 - 估价3.0 - 6.价格3.0销售等级生成  - http://wiki.huishoubao.com/web/#/138?page_id=15852
    入参：productId：产品机型id  |  evaType：质检类型，1-57标准质检，2-大质检，3-34标准质检，0-价格3.0
        optItem：机况答案选项id
    出参：productId：产品id
        levelId：价格3.0-定价等级id  |  levelName：价格3.0-定价等级名称
        saleLevelId：销售等级id  |  saleLevelName：销售等级名称  |  saleLevelDesc：销售等级描述
        baseLevelTag：价格3.0-定价等级标签
            baseLevelTag.tagId：定价等级标签id  |  baseLevelTag.tagName：定价等级标签名称
        saleLevelTag：价格3.0-销售等级标签
            saleLevelTag.tagId：销售等级标签id  |  saleLevelTag.tagName：销售等级标签名称
'''

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def v3_sale_evaluate(productId, evaType, optItem):
    """

    :param productId:
    :param evaType:
    :param optItem:
    :return:
    """
    param = {"_head":{"_interface":"sales_level_generation","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"1525332832","_invokeId":"152533283241636","_callerServiceId":"216002","_groupNo":"1"},"_param":{"productId":productId, "evaType":evaType, "optItem":optItem}}
    secret_key = "rAfnRwyWfh2N9vXVgWwdpJxaXgOCd8af"
    callerserviceid = "216002"
    url = "http://codserver.huishoubao.com/detect_v3/sales_level_generation"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    respone.encoding = respone.apparent_encoding  # 编码设置
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    ''' 1. 基础情况   '''
    # 1. 机况传空 | "_errStr":"请求参数错误 [OptItem必须至少包含1项]","_errCode":"70023100"
    # v3_sale_evaluate(productId='41567', evaType='0', optItem=[])
    # v3_sale_evaluate(productId='41567', evaType='', optItem=['8359']) #"_errStr":"请求参数错误 [EvaType为必填字段]","_errCode":"70023100"
    # v3_sale_evaluate(productId='41567', evaType='20210831', optItem=['8359']) #"_errStr":"请求参数错误 [EvaType必须是[0 1 2 3]中的一个]","_errCode":"70023100"

    ''' 2. evaType='0'  价格3.0   '''
    # v3_sale_evaluate(productId='41567', evaType='0', optItem=['8162','8351','8359','8148','8173','8323','8315','8090','8290','8101'])
    # v3_sale_evaluate(productId='41567', evaType='0', optItem=['8305'])

    ''' 3. evaType='1'  1-57标准质检   '''
    v3_sale_evaluate(productId='41567', evaType='1', optItem=['7446']) # "levelId":"570","levelName":"A3","saleLevelId":"570","saleLevelName":"A3"
    # v3_sale_evaluate(productId='41567', evaType='1', optItem=['8054']) # "levelId":"460","levelName":"C1","saleLevelId":"500","saleLevelName":"C+1"
    # v3_sale_evaluate(productId='41567', evaType='1', optItem=['8054','8054']) # "_errStr":"请求参数错误 [Key: 'SubsysReqBody.Param.OptItem' Error:Field validation for 'OptItem' failed on the 'unique' tag]","_errCode":"70023100"
    # v3_sale_evaluate(productId='41567', evaType='1', optItem=['8054','7500']) # "levelId":"422","levelName":"C12","saleLevelId":"450","saleLevelName":"C2"

    ''' 4. evaType='2'  2-大质检   '''
    # v3_sale_evaluate(productId='41567', evaType='1', optItem=['7446'])

    ''' 4. evaType='3'  3-34标准质检   '''
    # v3_sale_evaluate(productId='41567', evaType='3', optItem=['9026']) #"levelId":"600","levelName":"S","saleLevelId":"600","saleLevelName":"S"
    v3_sale_evaluate(productId='41567', evaType='3', optItem=['9040','9029']) #"_errStr":"销售等级生成失败 [定价等级[569]未配置销售等级]","_errCode":"70023302"
    # v3_sale_evaluate(productId='41567', evaType='3', optItem=['9042']) #"levelId":"460","levelName":"C1","saleLevelId":"500","saleLevelName":"C+1"
'''
【EvaluateConfV3】 【前提：定价等级模板 要切换到 定价等级标准】

一、evaType='0'  价格3.0
{"_head": {"_interface": "sales_level_generation", "_msgType": "request", "_remark": "", "_version": "0.01", "_timestamps": "1525332832", "_invokeId": "152533283241636", "_callerServiceId": "216002", "_groupNo": "1"}, "_param": {"productId": "41567", "evaType": "0", "optItem": ["8162", "8351", "8359", "8148", "8173", "8323", "8315", "8090", "8290", "8101"]}}
formParam: {ProductId:41567 EvaType:0 OptItem:[8162 8351 8359 8148 8173 8323 8315 8090 8290 8101]}

机况-匹配价格等级标准开始 ...
    optItem: [8162 8351 8359 8148 8173 8323 8315 8090 8290 8101]
    levelOrderMap: map[0:600 1:590 2:580 3:570 4:530 5:520 6:510 7:460 8:450 9:440 10:430 11:429 12:428 13:427 14:426 15:425 16:424 17:423 18:422 19:370 20:360 21:350 22:340 23:330 24:329 25:328 26:327 27:270 28:260 29:250 30:240 31:230 32:220 33:210 34:200 35:190 36:189 37:188 38:180 39:170 40:160 41:150 42:149 43:148 44:147 45:140 46:130 47:120 48:110 49:100 50:90 51:80 52:70 53:60 54:50 55:40 56:39 57:38]
    levelSaleMap: map[38:50 39:50 40:60 50:60 60:60 70:90 80:90 90:100 100:100 110:130 120:130 130:140 140:140 147:170 148:170 149:170 150:170 160:180 170:180 180:180 188:210 189:210 190:210 200:220 210:220 220:220 230:260 240:260 250:270 260:270 270:270 327:350 328:350 329:350 330:350 340:360 350:360 360:360 370:370 422:450 423:450 424:450 425:450 426:450 427:460 428:460 429:480 430:480 440:490 450:490 460:500 510:510 520:520 530:530 570:570 580:580 590:590 600:600]
    matching!!!
    match order: 0, itemComb: [8359]
    match level: 600, saleLevel: 600
    rrdisCmd: hget V3BaseLevel 600: {"Id":600,"Name":"S","Status":1,"ClassId":1}
    rrdisCmd: hget V3SaleLevel 600: {"Id":600,"Name":"S","Desc":"","Status":1,"ClassId":1}
    rrdisCmd: hmget V3LevelLabel 8 7 11 10: [{"Id":8,"Name":"手机定价等级标签2","Status":1,"ClassId":1,"TypeId":1} {"Id":7,"Name":"手机定价等级标签1","Status":1,"ClassId":1,"TypeId":1} {"Id":11,"Name":"手机销售等级标签2","Status":1,"ClassId":1,"TypeId":2} {"Id":10,"Name":"手机销售等级标签1","Status":1,"ClassId":1,"TypeId":2}]
机况-匹配价格等级标准结束 ...

 {"_head":{"_callerServiceId":"216002","_groupNo":"1","_interface":"sales_level_generation","_invokeId":"152533283241636","_msgType":"response","_remark":"","_timestamps":"1630404828","_version":"0.01"},"_data":{"_errStr":"SUCCESS","_data":{"productId":"41567","levelId":"600","levelName":"S","saleLevelId":"600","saleLevelName":"S","saleLevelDesc":"","baseLevelTag":[{"tagId":"8","tagName":"手机定价等级标签2"},{"tagId":"7","tagName":"手机定价等级标签1"}],"saleLevelTag":[{"tagId":"11","tagName":"手机销售等级标签2"},{"tagId":"10","tagName":"手机销售等级标签1"}]},"_errCode":"0","_ret":"0"}}
 
二、evaType='1'  1-57标准质检
{"_head": {"_interface": "sales_level_generation", "_msgType": "request", "_remark": "", "_version": "0.01", "_timestamps": "1525332832", "_invokeId": "152533283241636", "_callerServiceId": "216002", "_groupNo": "1"}, "_param": {"productId": "41567", "evaType": "1", "optItem": ["7446"]}}
formParam: {ProductId:41567 EvaType:1 OptItem:[7446]}
机况-匹配价格等级模板开始 ...
    optItem: [7446]
    使用57项等级模板配置匹配等级
    levelOrderMap: map[0:600 1:590 2:580 3:570 4:569 5:530 6:520 7:510 8:509 9:508 10:507 11:506 12:505 13:460 14:450 15:440 16:430 17:429 18:428 19:427 20:426 21:425 22:424 23:423 24:422 25:419 26:418 27:417 28:416 29:415 30:414 31:413 32:412 33:411 34:409 35:408 36:370 37:360 38:350 39:340 40:330 41:329 42:328 43:327 44:326 45:325 46:324 47:270 48:260 49:250 50:240 51:230 52:229 53:228 54:227 55:220 56:210 57:200 58:190 59:189 60:188 61:187 62:186 63:185 64:184 65:183 66:182 67:181 68:179 69:178 70:177 71:176 72:180 73:170 74:160 75:150 76:149 77:148 78:147 79:146 80:145 81:144 82:140 83:130 84:120 85:110 86:109 87:108 88:107 89:106 90:105 91:104 92:100 93:90 94:80 95:70 96:69 97:68 98:67 99:66 100:65 101:64 102:60 103:50 104:40 105:39 106:38 107:37 108:36 109:35 110:34 111:33 112:30 113:20 114:10 115:9 116:8 117:7 118:6 119:5 120:4 121:3 122:2 123:31]
    matching!!!
    match order: 3, itemComb: [7446]
    match level: 570
    rrdisCmd: hget V3BaseLevel 570: {"Id":570,"Name":"A3","Status":1,"ClassId":1}
机况-匹配价格等级模板结束 ...
rrdisCmd: hget V3SaleLevel 570: {"Id":570,"Name":"A3","Desc":"","Status":1,"ClassId":1}

{"_head":{"_callerServiceId":"216002","_groupNo":"1","_interface":"sales_level_generation","_invokeId":"152533283241636","_msgType":"response","_remark":"","_timestamps":"1630405551","_version":"0.01"},"_data":{"_errStr":"SUCCESS","_data":{"productId":"41567","levelId":"570","levelName":"A3","saleLevelId":"570","saleLevelName":"A3","saleLevelDesc":"","baseLevelTag":[],"saleLevelTag":[]},"_errCode":"0","_ret":"0"}}

二、evaType='2'  2-大质检


三、evaType='3'  3-34标准质检
{"_head": {"_interface": "sales_level_generation", "_msgType": "request", "_remark": "", "_version": "0.01", "_timestamps": "1525332832", "_invokeId": "152533283241636", "_callerServiceId": "216002", "_groupNo": "1"}, "_param": {"productId": "41567", "evaType": "3", "optItem": ["9026"]}}
formParam: {ProductId:41567 EvaType:3 OptItem:[9026]}
rrdisCmd: hget V3SpuEvaLevelTemplateV25 41567: 15
机况-匹配价格等级模板开始 ...
    optItem: [9026]
    使用34项等级模板配置匹配等级
    levelOrderMap: map[0:600 1:590 2:580 3:570 4:569 5:530 6:520 7:510 8:509 9:508 10:507 11:506 12:505 13:460 14:450 15:440 16:430 17:429 18:428 19:427 20:426 21:425 22:424 23:423 24:422 25:419 26:418 27:417 28:416 29:415 30:414 31:413 32:412 33:411 34:409 35:408 36:370 37:360 38:350 39:340 40:330 41:329 42:328 43:327 44:326 45:325 46:324 47:270 48:260 49:250 50:240 51:230 52:229 53:228 54:227 55:220 56:210 57:200 58:190 59:189 60:188 61:187 62:186 63:185 64:184 65:183 66:182 67:181 68:179 69:178 70:177 71:176 72:180 73:170 74:160 75:150 76:149 77:148 78:147 79:146 80:145 81:144 82:140 83:130 84:120 85:110 86:109 87:108 88:107 89:106 90:105 91:104 92:100 93:90 94:80 95:70 96:69 97:68 98:67 99:66 100:65 101:64 102:60 103:50 104:40 105:39 106:38 107:37 108:36 109:35 110:34 111:33 112:30 113:20 114:10 115:9 116:8 117:7 118:6 119:5 120:4 121:3 122:2 123:31]
    matching!!!
    match order: 0, itemComb: [9026]
    match level: 600
    rrdisCmd: hget V3BaseLevel 600: {"Id":600,"Name":"S","Status":1,"ClassId":1}
机况-匹配价格等级模板结束 ...
rrdisCmd: hget V3SaleLevel 600: {"Id":600,"Name":"S","Desc":"","Status":1,"ClassId":1}
rrdisCmd: hmget V3LevelLabel 8 7 11 10: [{"Id":8,"Name":"手机定价等级标签2","Status":1,"ClassId":1,"TypeId":1} {"Id":7,"Name":"手机定价等级标签1","Status":1,"ClassId":1,"TypeId":1} {"Id":11,"Name":"手机销售等级标签2","Status":1,"ClassId":1,"TypeId":2} {"Id":10,"Name":"手机销售等级标签1","Status":1,"ClassId":1,"TypeId":2}]


{"_head":{"_callerServiceId":"216002","_groupNo":"1","_interface":"sales_level_generation","_invokeId":"152533283241636","_msgType":"response","_remark":"","_timestamps":"1630406727","_version":"0.01"},"_data":{"_errStr":"SUCCESS","_data":{"productId":"41567","levelId":"600","levelName":"S","saleLevelId":"600","saleLevelName":"S","saleLevelDesc":"","baseLevelTag":[{"tagId":"8","tagName":"手机定价等级标签2"},{"tagId":"7","tagName":"手机定价等级标签1"}],"saleLevelTag":[{"tagId":"11","tagName":"手机销售等级标签2"},{"tagId":"10","tagName":"手机销售等级标签1"}]},"_errCode":"0","_ret":"0"}}

'''