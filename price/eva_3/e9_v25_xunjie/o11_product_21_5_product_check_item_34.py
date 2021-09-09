#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 21.检测标准化产品信息  - http://wiki.huishoubao.com/index.php?s=/105&page_id=3295
    入参：_interface
            “product_check_item”：产品检测标准化信息请求
            “product_check_item_grayscale”：闲鱼验机
            “product_check_item_youpin”：闲鱼优品验机
            “product_check_item_34”, 34项检测标准
        productId：产品id
    出参：quotation：估出的定价价格,单位分  |  standPrice：初始化价格，基准价，单位分
        recordId：估价记录id, (id 会超过int(11)，请不要用int保存）  |  levelId：等级ID
    1-对应服务：server-evaluate_detect（服务器应用名：server-evaluate_detect）  |  2-对应URL http://codserver.huishoubao.com
'''

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test

def product_check_item_34(productId):
    param = {"_head": { "_interface":"product_check_item_34", "_msgType":"request", "_remark":"", "_version":"0.01", "_timestamps":"123456", "_invokeId":"123456", "_callerServiceId":"112006", "_groupNo":"1" },"_param": {"productId":productId}}
    secret_key = "gYt8YHmZVUtq9BxHzmNBQ0Eo7oGi8IKU"
    callerserviceid = "112006"
    url = "http://codserver.huishoubao.com/detect/product_check_item"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    respone.encoding = respone.apparent_encoding  # 编码设置
    print(respone.text)
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

    strSkuList = []
    strSkuDesc = ''
    for info in skuList:
        answerList = info['answerList']
        index = random.randint(0, len(answerList) - 1)
        strSkuList.append(answerList[index]['answerId'])
        strSkuDesc += '"' + info['questionName'] + ":" + answerList[index]['answerName'] + '",'

    print('接口响应『json』格式数据为：\n',json.dumps(respone_dict,ensure_ascii=False) + '\n' )
    print('检测sku选项-答案项ID（随机取）：\n', strSkuList)
    print()
    print('检测以上【sku】选项名称+答案项名称：\n', '{' + strSkuDesc[:-1] + '}' + '\n')
    print('检测机况选项-答案项ID（随机取）：\n', strCheckList)
    print()
    print('检测以上【机况】选项名称+答案项名称：\n', '{' + strCheckDesc[:-1] + '}' + '\n')
    print('接口响应时长：{0} 秒'.format(respone.elapsed.total_seconds()))

if __name__ == '__main__':
    # product_check_item_34(productId="41567")
    # product_check_item_34(productId="50859")
    # product_check_item_34(productId="30832")
    product_check_item_34(productId="3415")

''' 
响应内容解析：
skuList：【产品商品库SKU信息】对应新后台，product_lib_new ——> SPU列表 ——> SKU选项管理
checkList：【标准检测机况信息】对应新后台，机况检测模板 ——> (搜索：类目-手机，状态-开启）

测试环境：模板ID：25，模板名称：定价模板v1（苹果Face ID）  |  模板ID：26，模板名称：定价模板v1（安卓指纹面容的）

【34项标准检测】
SELECT t.Fvalid,t.* from t_pdt_use_check_template_34 t WHERE t.Fproduct_id = '65783';
SELECT * from t_check_option_template b where b.Ftemplate_id = '29';
SELECT pdt_use.Ftemplate_id, check_template.Ftemplate_id, check_template.Fitem_info 
	FROM t_pdt_use_check_template_34 AS pdt_use 
	LEFT JOIN t_check_option_template AS check_template ON pdt_use.Ftemplate_id = check_template.Ftemplate_id 
WHERE pdt_use.Fvalid = '1' and check_template.Fvalid = '1' and Fproduct_id = '65783';

【产品标准检测机况】【server-evaluate_detect】
SELECT Fitem_info FROM t_pdt_use_check_template_34 AS pdt_use LEFT JOIN t_check_option_template AS check_template ON pdt_use.Ftemplate_id = check_template.Ftemplate_id WHERE pdt_use.Fvalid=1 and check_template.Fvalid=1 and Fproduct_id=41567;
select Fid, Fname from t_check_question_item where Fid in(8996,8998,7421,8999,7859,9038,9046,7480,9000,9001,9061,9066,9002,9003,7551,9004,9005,7569,7573,7576,5179,7583,9006,9007,9008,9009,9010,9011,9013,7531);
select Fid, Fname, Fweight, Fsingle_flag from t_check_answer_item where Fid in(9015,9016,9019,9021,9022,9023,9024,9025,9026,9027,9028,9029,9030,9031,9032,9033,9034,9035,9036,9037,9039,9040,9041,9042,9043,9044,9045,9047,9048,9049,9050,9051,9052,9053,9054,9055,7481,9056,9057,9058,9059,9060,9062,9063,9064,9065,9067,9068,9069,9070,9071,9072,9073,9074,9075,7559,9076,9077,9078,9079,9080,7570,9081,7574,7575,9082,9083,9084,9085,9086,7589,9088,9090,9091,9092,9093,9094,9095,9096,9097,9098,9099,9100,9101,9102,9103,9104,9105,9106,9107,9108,9109,9110,9111,9112,9113,9116,9117,9118,9119,7532,7533,7534);

【sku】【base_product】调接口 pdt_sku_query
curl -H 'HSB-OPENAPI-SIGNATURE:ea262c6f1957269bcb371e59e7fdbdce' -H 'HSB-OPENAPI-CALLERSERVICEID:216008' -d '{"_head":{"_callerServiceId":"216008","_groupNo":"1","_interface":"pdt_sku_query","_invokeId":"fbbb1e5b9ac9bf891bcc8dfb5ca2905e","_msgType":"request","_remark":"","_timestamps":"1621669686","_version":"0.01"},"_param":{"info":{"combination":"0","productId":"41567"},"subInterface":"sku_option_combination_get"}}

select Fproduct_id, Fvalid_sku_id, Finvalid_sku_id, Fsku_group, Fversion from t_pdt_sku_map  where Fproduct_id=41567;
select Fid, Faid_list from t_pdt_sku  where Fid in (21451,.......)
select t_a.Fid as Faid, t_a.Fname as Faname, t_q.Fid as Fqid, t_q.Fname as Fqname  from t_eva_item_base as t_a, t_eva_item_base as t_q  where t_a.Fpid=t_q.Fid and t_a.Flevel=3 and t_q.Flevel=2 and t_a.Fid in (1083,1091,1124,12,13,130,14,15,17,1773,18,2236,2241,2242,36,38,42,471,6047,6116,7630,8012);
'''