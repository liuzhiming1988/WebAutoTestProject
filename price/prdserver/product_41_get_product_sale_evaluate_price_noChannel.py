#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 41.标准检测选项获取商品评估价和保底价 - http://wiki.huishoubao.com/index.php?s=/105&page_id=7271
    1. 对应服务：server-evaluate_detect（服务器应用名：server-evaluate_detect） |  2. 对应URL http://codserver.huishoubao.com

    入参：productId：必填，产品id | skuList：必填，sku答案选项 | checkList：必填，检测答案选项
        channelId：非必填，渠道id，不传时，获取固定的“定价专用平台（10000192）”的价格即评估价，可以不传，但不能传空【此场景，不传】
    出参：mapOptionList：转换出来的机况选项 | mapSkuList：转化后的sku选项
        evaluatePrice：商品评估价 | bottomPrice：保底价 | evaluateId：估价Id

    注意：获取的是固定的 “定价专用平台” 的价格
'''

import hashlib, requests,json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test, hsb_response_print

class  Get_Product_Sale_Evaluate_Price:
    def __init__(self):
        self.secret_key = "gYt8YHmZVUtq9BxHzmNBQ0Eo7oGi8IKU"
        self.callerserviceid = "112006"

    def product_check_item(self, productId):
        param = {"_head": { "_interface":"product_check_item", "_msgType":"request", "_remark":"", "_version":"0.01", "_timestamps":"123456", "_invokeId":"123456", "_callerServiceId":"112006", "_groupNo":"1" },"_param": {"productId":productId, "orderId":"" }}
        url = "http://codserver.huishoubao.com/detect/product_check_item"
        md5value = json.dumps(param) + "_" + self.secret_key
        headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":self.callerserviceid}
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
            # 以下只为打印输出随机取的检测标准化机况选项数据
            strCheckDesc += '"' + info['questionName'] + ":" + answerList[index]['answerName'] + '",'

        strSkuList = []
        strSkuDesc = ''
        for info in skuList:
            answerList = info['answerList']
            index = random.randint(0, len(answerList) - 1)
            strSkuList.append(answerList[index]['answerId'])
            # 以下只为打印输出随机取的检测标准化SKU选项数据
            strSkuDesc += '"' + info['questionName'] + ":" + answerList[index]['answerName'] + '",'

        # print('接口响应『json』格式数据为：\n', json.dumps(respone_dict, ensure_ascii=False),'\n')
        print('==========1. 检测【sku】答案项ID传参数据为（随机取）：\n',strSkuList)
        print()
        print('==========2. 检测【机况】答案项ID传参数据为（随机取）：\n',strCheckList)
        print()
        print('==========3. 以上【sku】+以上【机况】选项名称+答案项名称：\n', '{' + strSkuDesc + strCheckDesc[:-1] + '}' + '\n')
        return strSkuList, strCheckList

    def get_product_sale_evaluate_price(self, productId):
        (skuList, checkList) = self.product_check_item(productId=productId)
        # skuList = ['13', '130', '17', '2236', '38', '1091', '2242']
        # checkList = ['7420', '7422', '7425', '7428', '7432', '7439', '7443', '7447', '7450', '7452', '7460', '7463', '7465', '7467', '7471', '7475', '7482', '7489', '7491', '7493', '7500', '7507', '7514', '7517', '7522', '7528', '7533', '7537', '7541', '7548', '7555', '7556', '7559', '7562', '7571', '7574', '7578', '7581', '7587', '7589', '7606', '7614']
        param = {"_head":{"_interface":"get_product_sale_evaluate_price","_msgType":"request","_remark":"hello","_version":"0.01","_timestamps":"123","_invokeId":"111","_callerServiceId":"112006","_groupNo":"1"},"_param":{"productId":productId, "skuList":skuList, "checkList":checkList}}
        url = "http://codserver.huishoubao.com/detect/get_product_sale_evaluate_price"
        md5value = json.dumps(param) + "_" + self.secret_key
        headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":self.callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        hsb_response_print(respone=respone)

if __name__ == '__main__':
    product_41 = Get_Product_Sale_Evaluate_Price()
    # product_41.get_product_sale_evaluate_price(productId='41567')
    product_41.get_product_sale_evaluate_price(productId='4157')

'''
流程
SELECT Fanswer_id, Feva_id, Fweight FROM t_check_mapping_eva, t_eva_item_base  WHERE t_eva_item_base.Fid = t_check_mapping_eva.Feva_id AND t_check_mapping_eva.Fvalid=1 AND t_eva_item_base.Fvalid=1 AND t_check_mapping_eva.Fanswer_id IN (7419,7422,7426,7430,7434,7440,7443,7446,7449,7453,7461,7463,7464,7469,7470,7475,7481,7487,7492,7496,7501,7506,7515,7520,7525,7528,7534,7536,7541,7548,7555,7557,7560,7565,7570,7574,7579,7581,7586,7589,7600,7613);

curl -H 'HSB-OPENAPI-SIGNATURE:464a726712f1e42661e87e02bcd70804' -H 'HSB-OPENAPI-CALLERSERVICEID:216008' -d '{"_head":{"_callerServiceId":"216008","_groupNo":"1","_interface":"product_id_info_get","_invokeId":"6b99ca0c279e55d04713c136aa975f3b","_msgType":"request","_remark":"","_timestamps":"1604473554","_version":"0.01"},"_param":{"evaFlag":"1","fchannel_id":"","fproduct_id":"41567","platformType":"0"}}' http://prdserver.huishoubao.com/rpc/new_product_lib

curl -H 'HSB-OPENAPI-SIGNATURE:37c7cc3856502d48bf02766d38f77360' -H 'HSB-OPENAPI-CALLERSERVICEID:216008' -d '{"_head":{"_callerServiceId":"216008","_groupNo":"1","_interface":"eva_option_get","_invokeId":"0cf839ad8aeb1e66028fe8240817eee3","_msgType":"request","_remark":"","_timestamps":"1604473554","_version":"0.01"},"_param":{"channel_id":"","pid":"","platform_type":"0","product_id":"41567"}}' http://prdserver.huishoubao.com/rpc/new_product_lib

curl -d '{"head":{"interface":"evaluateSecond","msgtype":"request","remark":"","version":"0.01"},"params":{"channel_id":"10000192","cookies":"server-evaluate_detect","ip":"127.0.0.1","isBottomPrice":"1","productid":"41567","select":["1078","3246","20","2170","24","224","56","5535","59","61","65","3247","6931","3244","3242","7642","82"],"userid":"0"}}' http://evaserver.huishoubao.com/rpc/evaluate
    hit cache time:1604473171 PId:0 tagId:0 channelId:10000192 channelFlag:1 platformId:9 platformName:定价专用平台
    productId:41567 pId: channelId:10000192 platformType:9
    
    select Fstandard_price, Fbasic_price, Frick_guarantee, Fneed_evaluate, Fproduct_id, Fitem_param_id, Fvalid, Fmax_price, Fsku_map, Fitem_template_id from t_eva_standard_product where Fproduct_id=41567 and Fdelete_flag = 1;
    select Fevaluate_item, Fversion, Fitem_group, Fitem_add_sub, Falgorithm_order, Fall_combination_price from t_eva_item_params  where Fid = 11812 and Fdelete_flag = 1;
    
    select Fstandard_price, Fbasic_price, Frick_guarantee, Fprice_control, Fneed_evaluate, Fproduct_id, Fitem_param_id, Fos_type, Fvalid, Fuse_standard_eva, Fmax_price, Fsku_map, Fitem_template_id from t_eva_platform_product where Fproduct_id=41567 and Fplatform_type=9 and Fdelete_flag = 1;
    
select Fchannel_id, Faddition, Fversion, Fvalid, Fdelete_flag, Foperator_name, Faddition_range from t_eva_channel_addition  where Fchannel_id = 10000192 and Fdelete_flag = 1;

select tbp.Fproduct_id, tbbr.Frule_info, tbbr.Fmin_price, tbbr.Fvalid from t_bangmai_product tbp, t_bangmai_bottom_rule tbbr where tbp.Fbottom_price_rule_id=tbbr.Fid and tbp.Fproduct_id = 41567;
    输入值:100 最低价:1100 选定保底价区间, 起始值:0 终止值:3000 类型:2 值:0 100+0=100 保底价小于最低价,改为1100
'''