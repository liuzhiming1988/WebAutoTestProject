#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 24.获取检测标准化选项  - http://wiki.huishoubao.com/web/#/105?page_id=4597

    1-对应服务：server-evaluate_detect（服务器应用名：server-evaluate_detect）  |  2-对应URL http://codserver.huishoubao.com

    统一get_check_item接口出参格式,当答案项不存在时,childs空数组输出
    -- 检测标准化问题项表   Fvalid：是否可用(1-可用）
	-- SPU列表，启用状态下，第1条开始，展示10个问题项，当某问题项不存在时，childs返回空数组
	SELECT SQL_CALC_FOUND_ROWS Fid, Fname from t_check_question_item where Fvalid=1 LIMIT 15,15; -- 启用状态，第16条开始，展示15个问题项
	SELECT SQL_CALC_FOUND_ROWS Fid, Fname from t_check_question_item where Fvalid=1  LIMIT 30,15 -- 启用状态，第31条开始，展示15个问题项
	SELECT * from t_check_question_item where Fvalid=1 LIMIT 0,10;
	-- 检测标准化答案项表
	SELECT Fid, Fquestion_id, Fname from t_check_answer_item where Fvalid=1 and Fquestion_id in (1,5003,5004,5005,5022,5023,5024,5031,5032,5036);
	SELECT Fid, Fquestion_id, Fname from t_check_answer_item where Fvalid=1 and Fquestion_id in (5079,5080,5081,5082,5083,5092,5093,5094,5100,5105,5110,5133,5154,5155,5172)

    pageIndex：分页的页码；   pageSize：每页的数量; 当答案项不存在时,childs空数组输出
'''

import hashlib, requests, json, os
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def get_check_item(classId):
    param = {"_head":{ "_interface":"get_check_item", "_msgType":"request", "_remark":"", "_version":"0.01", "_timestamps":"1525332832", "_invokeId":"SALESDETECT152533283241636", "_callerServiceId":"112006", "_groupNo":"1"},"_param":{"pageIndex":"0", "pageSize":"500", "classId":classId}}

    secret_key = "gYt8YHmZVUtq9BxHzmNBQ0Eo7oGi8IKU"
    callerserviceid = "112006"
    url = "http://codserver.huishoubao.com/detect/check_itemList"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    # get_check_item(classId='1')
    # get_check_item(classId='1#2')
    # get_check_item(classId='1#2#10')
    get_check_item(classId='1#2#10#111111111')
    # get_check_item(classId='')

'''
测试
SELECT SQL_CALC_FOUND_ROWS Fid, Fname from t_check_question_item where Fvalid=1  and Fclass_id IN (1) LIMIT 0,500;
 SELECT FOUND_ROWS();
SELECT Fid, Fquestion_id, Fname from t_check_answer_item where Fvalid=1 and Fquestion_id in (7,11,16,19,22,51,54,57,60,64,67,72,76,81,222,1076,1461,2169,5003,5004,5005,5022,5023,5024,5036,5037,5040,5042,5043,5046,5047,5048,5050,5051,5053,5060,5064,5069,5070,5072,5073,5074,5076,5077,5078,5079,5080,5081,5082,5083,5092,5093,5094,5100,5105,5110,5154,5155,5172,5179,5185,5193,5200,5230,5533,6701,6929,7263,7421,7424,7427,7431,7435,7441,7444,7448,7451,7454,7455,7456,7457,7458,7459,7480,7484,7485,7486,7498,7505,7509,7516,7521,7527,7531,7535,7540,7546,7549,7550,7551,7552,7569,7573,7576,7577,7582,7583,7584,7585,7598,7612,7640,7790,7794,7800,7856,7859,7863,7867,7868,7869,7870,7871,7872,7873,7874,7875,7876,7965);
'''