#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 53.获取检测标准化产品信息【产品商品库sku信息 + 标准检测机况信息】（53）  - http://wiki.huishoubao.com/index.php?s=/105&page_id=3295

    1-对应服务：server-evaluate_detect（服务器应用名：server-evaluate_detect）  |  2-对应URL http://codserver.huishoubao.com
'''

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test

def product_check_item_youpin_v2(productId):
    param = {"_head": { "_interface":"product_check_item_youpin_v2", "_msgType":"request", "_remark":"", "_version":"0.01", "_timestamps":"123456", "_invokeId":"123456", "_callerServiceId":"112006", "_groupNo":"1" },"_param": {"productId":productId}}

    secret_key = "gYt8YHmZVUtq9BxHzmNBQ0Eo7oGi8IKU"
    callerserviceid = "112006"
    url = "http://codserver.huishoubao.com/detect/product_check_item"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    respone.encoding = respone.apparent_encoding  # 编码设置
    respone_dict = json.loads(respone.text)  # 转成字典
    print(respone.text)
    checkList = respone_dict['_data']['_data']['checkList']
    skuList = respone_dict['_data']['_data']['skuList']

    strCheckList = ''
    strCheckDesc = ''
    for info in checkList:
        answerList = info['answerList']
        index = random.randint(0, len(answerList) - 1)
        strCheckList += '"' + answerList[index]['answerId'] + '",'
        strCheckDesc += '"' + info['questionName'] + ":" + answerList[index]['answerName'] + '",'
    strCheckList = strCheckList[:-1]

    strSkuList = ''
    strSkuDesc = ''
    for info in skuList:
        answerList = info['answerList']
        index = random.randint(0, len(answerList) - 1)
        strSkuList += '"' + answerList[index]['answerId'] + '",'
        strSkuDesc += '"' + info['questionName'] + ":" + answerList[index]['answerName'] + '",'
    strSkuList = strSkuList[:-1]

    print('接口响应『json』格式数据为：\n',json.dumps(respone_dict,ensure_ascii=False) + '\n' )
    print('检测sku选项-答案项ID（随机取）：\n', '{' + strSkuList + '}' + '\n')
    print('检测机况选项-答案项ID（随机取）：\n', '{' + strCheckList + '}' + '\n')
    print('检测以上【sku】+以上【机况】选项名称+答案项名称：\n', '{' + strSkuDesc + strCheckDesc[:-1] + '}' + '\n')
    print('接口响应时长：{0} 秒'.format(respone.elapsed.total_seconds()))

if __name__ == '__main__':
    # product_check_item_youpin_v2(productId="")
    # product_check_item_youpin_v2(productId="111111111111")
    product_check_item_youpin_v2(productId="41567")
    # product_check_item_youpin_v2(productId="64000")
    # product_check_item_youpin_v2(productId="30748")
    # product_check_item_youpin_v2(productId="65783")

''' 
响应内容解析：
skuList：【产品商品库SKU信息】对应新后台，product_lib_new ——> SPU列表 ——> SKU选项管理
checkList：【标准检测机况信息】对应新后台，机况检测模板 ——> (搜索：类目-手机，状态-开启）

【闲鱼无忧购验机2.0】
SELECT t.Fvalid,t.* from t_pdt_use_check_template_youpin_v2 t WHERE Fproduct_id = '65743';
SELECT * from t_check_option_template b where b.Ftemplate_id = '24';
SELECT pdt_use.Ftemplate_id, check_template.Ftemplate_id, check_template.Fitem_info 
	FROM t_pdt_use_check_template_youpin_v2 AS pdt_use 
	LEFT JOIN t_check_option_template AS check_template ON pdt_use.Ftemplate_id = check_template.Ftemplate_id 
WHERE pdt_use.Fvalid = '1' and check_template.Fvalid = '1' and Fproduct_id = '65783';


select Fid, Fname from t_check_question_item where Fid in(7263,7421,7424,7427,7431,7435,7441,7444,7448,7451,7454,7456,7455,7457,7458,7459,7480,7484,7485,7486,7498,7505,7509,7516,7521,7527,7531,7535,7540,7546,7549,7551,7550,7552,7569,7573,7576,7577,7582,7583,7598,7612,7790,7794);

select Fid, Fname, Fweight, Fsingle_flag from t_check_answer_item where Fid in(7418,7419,7420,7422,7423,7425,7426,7428,7429,7430,7432,7433,7434,7436,7437,7438,7439,7440,7442,7443,7445,7446,7447,7449,7450,7452,7453,7460,7461,7464,7465,7466,7462,7463,7467,7468,7469,7470,7471,7472,7473,7474,7475,7476,7477,7478,7479,7481,7482,7483,7487,7488,7489,7490,7491,7492,7493,7494,7495,7496,7497,7499,7500,7501,7502,7503,7504,7506,7507,7508,7510,7511,7512,7513,7514,7515,7517,7518,7519,7520,7522,7523,7524,7525,7526,7528,7529,7530,7615,7532,7533,7534,7536,7537,7538,7539,7541,7542,7543,7544,7545,7547,7548,7553,7554,7555,7559,7560,7561,7556,7557,7558,7562,7563,7564,7565,7566,7570,7571,7572,7574,7575,7578,7579,7580,7581,7586,7587,7588,7589,7590,7591,7599,7600,7601,7602,7603,7604,7605,7606,7607,7608,7609,7610,7611,7613,7614,7791,7792,7793,7795,7796);

curl -H 'HSB-OPENAPI-SIGNATURE:79c7c4cec91b558fe388cb7267a5a9da' -H 'HSB-OPENAPI-CALLERSERVICEID:216008' -d '{"_head":{"_callerServiceId":"216008","_groupNo":"1","_interface":"pdt_sku_query","_invokeId":"9c8dd5dbebdd10ab44195db26aa4f558","_msgType":"request","_remark":"","_timestamps":"1612495162","_version":"0.01"},"_param":{"info":{"combination":"0","productId":"41567"},"subInterface":"sku_option_combination_get"}}' http://prdserver.huishoubao.com/rpc/new_product_lib
'''