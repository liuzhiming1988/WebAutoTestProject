#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : v2_outprice_sale_apply_price.py
@Author  : liuzhiming
@Time    : 2021/10/8 15:27
"""

"""
拍机堂实时爬价需求
需求：
https://www.tapd.cn/21967291/prong/stories/view/1121967291001062801
接口：
获取选项：http://wiki.huishoubao.com/web/#/105?page_id=3295
获取销售价：http://wiki.huishoubao.com/web/#/138?page_id=15625
服务：k8s   basepriceevaluate
"""

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print, hsb_eva_ipProxy_k8s_test


class V3SaleEvaluateOutPrice:

    def __init__(self):
        self.secret_key = "gYt8YHmZVUtq9BxHzmNBQ0Eo7oGi8IKU"
        self.service_id = "112006"

    def product_check_item_34(self, product_id="41567"):
        param = {"_head": {"_interface": "product_check_item_34", "_msgType": "request", "_remark": "", "_version": "0.01","_timestamps": "1525332832", "_invokeId": "152533283241636", "_callerServiceId": self.service_id,"_groupNo": "1"},
                 "_param": {"productId": product_id}}
        url = "http://codserver.huishoubao.com/detect/product_check_item"
        md5value = json.dumps(param) + "_" + self.secret_key
        headers = {"Content-Type": "application/json;charset=UTF-8", "HSB-OPENAPI-SIGNATURE": Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID": self.service_id}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置
        respone_dict = json.loads(respone.text)  # 转成字典
        print(respone_dict)
        checkList = respone_dict['_data']['_data']['checkList']
        skuList = respone_dict['_data']['_data']['skuList']

        strCheckList = []
        strCheckDesc = ''
        for info in checkList:
            answerList = info['answerList']
            print("答案项列表{}".format(answerList))
            '''第一种方式：在answerList下随机取1个'''
            # index = random.randint(0, len(answerList) - 1)
            index = 0
            strCheckList.append(answerList[index]['answerId'])
            strCheckDesc += '"' + info['questionName'] + ":" + answerList[index]['answerName'] + '",'

            '''第二种方式：在answerList下取answerWeight最大的那个'''
            # index = sorted(answerList, key=lambda x: int(x['answerWeight']), reverse=True)[0]
            # strCheckList.append(index['answerId'])
            # strCheckDesc += '"' + info['questionName'] + ":" + index['answerName'] + '",'

        strSkuList = []
        strSkuDesc = ''
        for info in skuList:
            answerList = info['answerList']
            # index = random.randint(0, len(answerList) - 1)
            index =0
            strSkuList.append(answerList[index]['answerId'])
            strSkuDesc += '"' + info['questionName'] + ":" + answerList[index]['answerName'] + '",'
        # print("====={}\n{}\n\n====={}\n{}".format(strSkuList, strSkuDesc, strCheckList, strCheckDesc))
        return strSkuList, strSkuDesc, strCheckList, strCheckDesc

    def sale_apply_price(self, planId, product_id, evaType, strSkuList, strCheckList, useOutPrice="0",
                         channelId="3", ip="127.0.0.1", freqLimitType="0"):

        # (strSkuList, strSkuDesc, strCheckList, strCheckDesc) = self.product_check_item_34(product_id=product_id)

        param = {"_head": {"_interface": "sale_apply_price", "_msgType": "request", "_remark": "", "_version": "0.01",
                           "_timestamps": "1525332832", "_invokeId": "467891346879-999999",
                           "_callerServiceId": "116006", "_groupNo": "1"},
                 "_param": {"planId": planId, "productId": product_id, "evaType": evaType, "skuItem": strSkuList,
                            "optItem": strCheckList, "ip": ip, "userId": "1895", "freqLimitType": freqLimitType,
                            "useOutPrice": useOutPrice, "outPrice": {"channelId": channelId, "planId": "3"}}}
        print(json.dumps(param))
        secret_key = "R2gFCRbILiNhwv3YbtaGceYJlPS5Ku02"
        callerserviceid = "116006"
        url = "http://bpeserver.huishoubao.com/adjustment_price/sale_apply_price"
        md5value = json.dumps(param) + "_" + secret_key
        headers = {"Content-Type": "application/json;charset=UTF-8", "HSB-OPENAPI-SIGNATURE": Md5Enerypt(md5value),
                   "HSB-OPENAPI-CALLERSERVICEID": callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_k8s_test())

        print('========>1.『{0}』 产品的『检测标准化选项-sku』(随机取)为：\n'.format(product_id), strSkuList)
        # print('\n========>2. 以上『检测标准化选项-sku』为：\n', '{' + strSkuDesc[:-1] + '}')
        print('\n========>3.『{0}』 产品的『检测标准化选项-机况-34』(随机取)为：\n'.format(product_id), strCheckList)
        # print('\n========>4. 以上『检测标准化选项-机况-34』为：\n', '{' + strCheckDesc[:-1] + '}')
        hsb_response_print(respone=respone)

    def auto_get_sale_apply_price(self):
        pass


if __name__ == '__main__':
    sale_out_price = V3SaleEvaluateOutPrice()
    # sale_out_price.product_check_item_34(product_id="41567")  # 获取选项
    # sku_list = ['7630', '130', '18', '2236', '38', '1091', '1083']
    # opt_list = ['9015', '9019', '9027', '9028', '9035', '9039', '9047', '7481', '9057', '9059', '9062', '9067',
    #              '9071', '9074', '7559', '9077', '7570', '7574', '9082', '9084', '7589', '9090', '9094', '9098',
    #              '9102', '9106', '9111', '9117', '9120']

    # sku_list = ['8012', '130', '18', '2236', '36', '1091', '2242']
    # opt_list = ['9015', '9019', '9025', '9031', '9037', '9043', '9047', '7481', '9058', '9059', '9062', '9067',
    #             '9071', '9075', '7559', '9078', '7570', '7575', '9082', '9084', '7589', '9092', '9096', '9098',
    #             '9104', '9110', '9111', '9117', '9120']

    # sku_list = ['7630', '130', '17', '2236', '36', '1091', '2242']
    # opt_list = ['9016', '9021', '9026', '9030', '9037', '9044', '9047', '9056', '9058', '9060', '9062', '9067',
    #             '9072', '9075', '7559', '9078', '9081', '7575', '9083', '9086', '9088', '9090', '9097', '9098',
    #             '9104', '9110', '9111', '9117', '9120']

    sku_list = ['12', '130', '17', '2236', '36', '42', '1083']
    opt_list = ['9015', '9019', '9025', '9028', '9035', '9039', '9047', '7481', '9057', '9059', '9062', '9067',
                '9071', '9074', '7559', '9077', '7570', '7574', '9082', '9084', '7589', '9090', '9094', '9098',
                '9102', '9106', '9111', '9117', '9120']

    sale_out_price.sale_apply_price(planId="3", product_id="41567", evaType="3", useOutPrice="1", channelId="3",
                                    strSkuList=sku_list, strCheckList=opt_list)

    # sku_list = ["12","2236","36","42","17","130","1083"]
    # opt_list = ["9019","9015","9026","9031","9035","9039","9047","7481","9059","9071","9062","9067","9057","9074","7559","9077","9079","7574","7570","9082","9084","7586","9102","9098","9091","9094","9106","9120","9111","9116"]
    # # opt_list = ['9016', '9019', '9026', '9031', '9037', '9042', '9049', '9056', '9057', '9059', '9062', '9069', '9072', '9075', '7559', '9078', '9079', '9081', '7574', '9082', '9085', '7586', '9093', '9096', '9098', '9104', '9109', '9113', '9118', '9120']
    # sale_out_price.sale_apply_price(planId="3", product_id="38201", evaType="3", useOutPrice="0", channelId="3",
    #                                 strSkuList=sku_list, strCheckList=opt_list)


