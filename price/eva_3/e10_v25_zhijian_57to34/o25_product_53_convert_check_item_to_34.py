#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 53.标准检测57项转34项 - http://wiki.huishoubao.com/web/#/105?page_id=15861
    1. 对应服务：server-evaluate_detect（服务器应用名：server-evaluate_detect） |  2. 对应URL http://codserver.huishoubao.com

    入参：productId：产品id  |  skuList：sku答案选项  |  checkList：检测答案选项
    出参：productId：产品id  |  transform34List：转换出来的选项详细信息
            productId.queId：问题项id  |  productId.queName：问题项名称
            productId.ansId：答案项id  |  productId.ansName：答案项名称
            productId.confType：选项类型 1-sku；2-机况
'''

import hashlib, requests,json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test, hsb_response_print

class  Convert_Check_Item_To_34:
    def __init__(self):
        self.secret_key = "gYt8YHmZVUtq9BxHzmNBQ0Eo7oGi8IKU"
        self.callerserviceid = "112006"

    def product_check_item_57(self, productId):
        param = {"_head": { "_interface":"product_check_item", "_msgType":"request", "_remark":"product_check_item_34", "_version":"0.01", "_timestamps":"123456", "_invokeId":"123456", "_callerServiceId":"112006", "_groupNo":"1" },"_param": {"productId":productId, "orderId":"" }}
        url = "http://codserver.huishoubao.com/detect/product_check_item"
        md5value = json.dumps(param) + "_" + self.secret_key
        headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":self.callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置
        respone_dict = json.loads(respone.text)  # 转成字典
        # print("获取的57项检测选项为：\n{}".format(respone_dict))
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

    def convert_check_item_to_34 (self, productId):
        (skuList, checkList) = self.product_check_item_57(productId=productId)

        # 苹果机型，iPhone X
        # skuList = ["6116", "130", "18", "2236", "36", "42", "2242"]

        # 安卓机型，华为 P40（5G）
        # skuList = ["6116", "130", "18", "2236", "36", "42", "2242"]

        # SKU特殊情况验证
        # skuList = []
        # skuList = ["6116", "130", "18", "2236", "36", "42", "2242"]


        ''' 1. 第一次随机核验的数据'''
        # checkList = ["7420", "7423", "7425", "7430", "7432", "7437", "7442", "7447", "8055", "7452", "7460", "7463", "7464", "7468", "7470", "7474", "7482", "7487", "7491", "7495", "7500", "7508", "7514", "7519", "7526", "7615", "7532", "7536", "7544", "7548", "7553", "7557", "7559", "7562", "7571", "7575", "7579", "7581", "7588", "7589", "7599", "7613", "9084"]

        ''' 2. 7428 且 7432 且 7436 且 7442 且（非7519），走 命中9028 分支'''
        # checkList = ["7420", "7423", "7425",   "7428", "7432", "7436", "7442",   "7437", "7447", "8055", "7452", "7460", "7463", "7464", "7468", "7470", "7474", "7482", "7487", "7491", "7495", "7500", "7508", "7514",   "7517",   "7526", "7615", "7532", "7536", "7544", "7548", "7553", "7557", "7559", "7562", "7571", "7575", "7579", "7581", "7588", "7589", "7599", "7613", "9084"]

        ''' 3. 7428 且 7432 且 7436 且 7442 且（7519），不会走 命中 9028 分支'''
        # checkList = ["7420", "7423", "7425",   "7428", "7432", "7436", "7442",   "7437", "7447", "8055", "7452", "7460", "7463", "7464", "7468", "7470", "7474", "7482", "7487", "7491", "7495", "7500", "7508", "7514",   "7519",   "7526", "7615", "7532", "7536", "7544", "7548", "7553", "7557", "7559", "7562", "7571", "7575", "7579", "7581", "7588", "7589", "7599", "7613", "9084"]

        ''' 4. 7443 且 （7438 或 7439 或 7440 或 7519），走 命中 9034 分支'''
        # checkList = ["7420", "7423", "7425", "7428", "7432", "7436",   "7443", "7438",   "7447", "8055", "7452", "7460", "7463", "7464", "7468", "7470", "7474", "7482", "7487", "7491", "7495", "7500", "7508", "7514",   "7517",   "7526", "7615", "7532", "7536", "7544", "7548", "7553", "7557", "7559", "7562", "7571", "7575", "7579", "7581", "7588", "7589", "7599", "7613", "9084"]

        ''' 5. 7443  且 （7438 或 7439 或 7440 或 7519），7443 且7438 且7439，同样走 命中 9034 分支'''
        # checkList = ["7420", "7423", "7425", "7428", "7432", "7436",   "7443", "7438", "7439",   "7447", "8055", "7452", "7460", "7463", "7464", "7468", "7470", "7474", "7482", "7487", "7491", "7495", "7500", "7508", "7514",   "7517",   "7526", "7615", "7532", "7536", "7544", "7548", "7553", "7557", "7559", "7562", "7571", "7575", "7579", "7581", "7588", "7589", "7599", "7613", "9084"]

        ''' 6. 7445 且 7449 且 7452，命中 9039 分支'''
        # checkList = ["7420", "7423", "7425", "7428", "7432", "7436", "7443", "7438", "7439",   "7445", "7449", "7452",   "7460", "7463", "7464", "7468", "7470", "7474", "7482", "7487", "7491", "7495", "7500", "7508", "7514", "7517", "7526", "7615", "7532", "7536", "7544", "7548", "7553", "7557", "7559", "7562", "7571", "7575", "7579", "7581", "7588", "7589", "7599", "7613", "9084"]

        ''' 7. 7445 且 7449 没有且 7452，不会走 命中 9039 分支'''
        # checkList = ["7420", "7423", "7425", "7428", "7432", "7436", "7443", "7438", "7439",   "7445", "7449", "7453",   "7460", "7463", "7464", "7468", "7470", "7474", "7482", "7487", "7491", "7495", "7500", "7508", "7514", "7517", "7526", "7615", "7532", "7536", "7544", "7548", "7553", "7557", "7559", "7562", "7571", "7575", "7579", "7581", "7588", "7589", "7599", "7613", "9084"]

        ''' 8. 7460 且 7464 且 7462 且 7470 且 7467 且 7473， 命中 9047 分支'''
        # checkList = ["7420", "7423", "7425", "7428", "7432", "7436", "7443", "7438", "7439", "7445", "7449", "7453",   "7460", "7462", "7464", "7467", "7470", "7473",   "7482", "7487", "7491", "7495", "7500", "7508", "7514", "7517", "7526", "7615", "7532", "7536", "7544", "7548", "7553", "7557", "7559", "7562", "7571", "7575", "7579", "7581", "7588", "7589", "7599", "7613", "9084"]

        ''' 9. 7460 且 7464 且 7462 且 7470 且 7467 没有且 7473， 不会走 命中 9047 分支'''
        # checkList = ["7420", "7423", "7425", "7428", "7432", "7436", "7443", "7438", "7439", "7445", "7449", "7453",   "7460", "7462", "7464", "7467", "7470", "7474",   "7482", "7487", "7491", "7495", "7500", "7508", "7514", "7517", "7526", "7615", "7532", "7536", "7544", "7548", "7553", "7557", "7559", "7562", "7571", "7575", "7579", "7581", "7588", "7589", "7599", "7613", "9084"]

        ''' 10. 非（7600 或 7601 或 7602）， 命中 9090 分支'''
        # checkList = ["7420", "7423", "7425", "7428", "7432", "7436", "7443", "7438", "7439", "7445", "7449", "7453", "7460", "7462", "7464", "7467", "7470", "7474", "7482", "7487", "7491", "7495", "7500", "7508", "7514", "7517", "7526", "7615", "7532", "7536", "7544", "7548", "7553", "7557",   "7559",   "7562", "7571", "7575", "7579", "7581", "7588", "7589", "7599", "7613", "9084"]

        ''' 11. 非（7600 或 7601 或 7602），有 7600 或 7601 或 7602 ， 不会命中 9090 分支'''
        # checkList = ["7420", "7423", "7425", "7428", "7432", "7436", "7443", "7438", "7439", "7445", "7449", "7453", "7460", "7462", "7464", "7467", "7470", "7474", "7482", "7487", "7491", "7495", "7500", "7508", "7514", "7517", "7526", "7615", "7532", "7536", "7544", "7548", "7553", "7557",   "7600",   "7562", "7571", "7575", "7579", "7581", "7588", "7589", "7599", "7613", "9084"]

        ''' 12. （7522 或 7526） 且 （7528 或 7615） ， 命中 9057 分支'''
        # checkList = ["7420", "7423", "7425", "7428", "7432", "7436", "7443", "7438", "7439", "7445", "7449", "7453", "7460", "7462", "7464", "7467", "7470", "7474", "7482", "7487", "7491", "7495", "7500", "7508", "7514", "7517",    "7522", "7615",   "7532", "7536", "7544", "7548", "7553", "7557", "7600", "7562", "7571", "7575", "7579", "7581", "7588", "7589", "7599", "7613", "9084"]
        # checkList = ["7420", "7423", "7425", "7428", "7432", "7436", "7443", "7438", "7439", "7445", "7449", "7453", "7460", "7462", "7464", "7467", "7470", "7474", "7482", "7487", "7491", "7495", "7500", "7508", "7514", "7517",    "7522", "7528",   "7532", "7536", "7544", "7548", "7553", "7557", "7600", "7562", "7571", "7575", "7579", "7581", "7588", "7589", "7599", "7613", "9084"]
        # checkList = ["7420", "7423", "7425", "7428", "7432", "7436", "7443", "7438", "7439", "7445", "7449", "7453", "7460", "7462", "7464", "7467", "7470", "7474", "7482", "7487", "7491", "7495", "7500", "7508", "7514", "7517",    "7522", "7529",   "7532", "7536", "7544", "7548", "7553", "7557", "7600", "7562", "7571", "7575", "7579", "7581", "7588", "7589", "7599", "7613", "9084"]

        ''' 12. 7536 且 （7541 或 7545）且 7547， 命中 9059 分支'''
        # checkList = ["7420", "7423", "7425", "7428", "7432", "7436", "7443", "7438", "7439", "7445", "7449", "7453", "7460", "7462", "7464", "7467", "7470", "7474", "7482", "7487", "7491", "7495", "7500", "7508", "7514", "7517", "7522", "7615", "7532",   "7536", "7541", "7547",   "7553", "7557", "7600", "7562", "7571", "7575", "7579", "7581", "7588", "7589", "7599", "7613", "9084"]
        # checkList = ["7420", "7423", "7425", "7428", "7432", "7436", "7443", "7438", "7439", "7445", "7449", "7453", "7460", "7462", "7464", "7467", "7470", "7474", "7482", "7487", "7491", "7495", "7500", "7508", "7514", "7517", "7522", "7615", "7532",   "7536", "7543", "7547",   "7553", "7557", "7600", "7562", "7571", "7575", "7579", "7581", "7588", "7589", "7599", "7613", "9084"]

        ''' 13. 【安卓机型】【华为 P40（5G）】'''
        # checkList = ["7420", "7422", "7425", "7428", "7434", "7436", "7443", "7446", "8055", "7452", "7460", "7463", "7466", "7467", "7471", "7479", "7481", "7489", "7490", "7495", "7503", "7506", "7513", "7518", "7522", "7530", "7532", "7538", "7542", "7548", "7555", "7556", "7559", "7568", "7570", "7575", "7578", "7581", "7586", "7592", "7596", "7609", "7613"]

        ''' 14. 【安卓机型】【华为 P40（5G）】【特殊机况情况测试】'''
        # checkList = []
        # checkList = ["7420", "7422", "7425", "7428", "7434", "7436", "7443", "7446", "8055", "7452", "7460", "7463", "7466", "7467", "7471", "7479", "7481", "7489", "7490", "7495", "7503", "7506", "7513", "7518", "7522", "7530", "7532", "7538", "7542", "7548", "7555", "7556", "7559", "7568", "7570", "7575", "7578", "7581", "7586", "7592", "7596", "7609", "7613"]

        param = {"_head":{"_version":"0.01","_msgType":"request","_invokeId":"convert_check_item_to_34","_remark":"","_interface":"convert_check_item_to_34","_timestamps":"1629908689","_callerServiceId":"112006","_groupNo":"1"},"_param":{"productId":productId, "skuList":skuList, "checkList":checkList}}
        print(param)
        url = "http://codserver.huishoubao.com/detect/convert_check_item_to_34"
        md5value = json.dumps(param) + "_" + self.secret_key
        headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":self.callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        hsb_response_print(respone=respone)

if __name__ == '__main__':
    product_53 = Convert_Check_Item_To_34()
    product_53.convert_check_item_to_34 (productId='41567') # 苹果机型  iPhone X
    # product_53.convert_check_item_to_34 (productId='64000') # 安卓机型 华为 P40（5G）
    # product_53.convert_check_item_to_34 (productId='64000') # 安卓机型 华为 P40（5G） | 不传sku  |  允许
    # product_53.convert_check_item_to_34 (productId='64000') # 安卓机型 华为 P40（5G） | 不传机况 |  允许，全部返回最好的
    # product_53.convert_check_item_to_34 (productId='23007')

'''
【质检报告切34项】【57转34】【server-evaluate_detect】 

SELECT Fitem_info FROM t_pdt_use_check_template_34 AS pdt_use 
    LEFT JOIN t_check_option_template AS check_template ON pdt_use.Ftemplate_id = check_template.Ftemplate_id 
WHERE pdt_use.Fvalid = 1 and check_template.Fvalid = 1 and Fproduct_id = 41567;

select Fid, Fname from t_check_question_item where Fid in(8996,8998,7421,8999,7859,9038,9046,7480,9000,9001,9061,9066,9002,9003,7551,9004,9005,7569,7573,7576,5179,7583,9006,9007,9008,9009,9010,9011,9013,9014)

select Fid, Fname, Fweight, Fsingle_flag from t_check_answer_item where Fid in(9015,9016,9019,9021,9022,9023,9024,9025,9026,9027,9028,9029,9030,9031,9032,9033,9034,9035,9036,9037,9039,9040,9041,9042,9043,9044,9045,9047,9048,9049,9050,9051,9052,9053,9054,9055,7481,9056,9057,9058,9059,9060,9062,9063,9064,9065,9067,9068,9069,9070,9071,9072,9073,9074,9075,7559,9076,9077,9078,9079,9080,7570,9081,7574,7575,9082,9083,9084,9085,9086,7589,9088,9090,9091,9092,9093,9094,9095,9096,9097,9098,9099,9100,9102,9103,9104,9106,9108,9109,9110,9111,9112,9113,9117,9118,9116,9119,9120,9121,9191)

SELECT Fanswer_id, Fanswer_id_34, Fweight FROM t_check_mapping_check34, t_check_answer_item 
    WHERE t_check_answer_item.Fid = t_check_mapping_check34.Fanswer_id_34 
    AND t_check_mapping_check34.Fvalid = 1 AND t_check_answer_item.Fvalid = 1 
    AND t_check_mapping_check34.Fanswer_id IN (7420,7423,7425,7430,7432,7437,7442,7447,8055,7452,7460,7463,7464,7468,7470,7474,7482,7487,7491,7495,7500,7508,7514,7519,7526,7615,7532,7536,7544,7548,7553,7557,7559,7562,7571,7575,7579,7581,7588,7589,7599,7613,9084)

SELECT A.Fid AS Fans_id, A.Fname AS Fans_name, A.Fweight, B.Fid AS Fque_id, B.Fname AS Fque_name 
    FROM t_eva_item_base A LEFT JOIN t_eva_item_base B ON A.Fpid = B.Fid WHERE A.Fid IN (6116,130,18,2236,36,42,2242)

SELECT A.Fid AS Fans_id, A.Fname AS Fans_name, A.Fweight, B.Fid AS Fque_id, B.Fname AS Fque_name 
    FROM t_eva_item_base A LEFT JOIN t_eva_item_base B ON A.Fpid = B.Fid WHERE A.Fid IN (6116,130,18,2236,36,42,2242)
'''