#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 估价产品后台 - 产品中心服务 - 3.产品标准sku获取 - http://wiki.huishoubao.com/index.php?s=/227&page_id=5902
	一层协议：server-evaluate_admin  二层：base_product
	入参：info：必填，配置信息 | productId：必填，产品id
		combination：非必填，获取有效无效sku组合的标记 可不传 默然为0
	出参：productId：产品id | combination：sku组合 | aIdList：组成sk的答案项 | skuId：skusId | valid：sku启用标记
		options：sku选项信息 | qName：问题项名称 | qId：问题项id | aInfo：答案项信息 | aId：答案项id | aName：答案项名称
'''

import json
from price.session_public_Amc_login import session_public_Amc_login
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def sku_option_combination_get(productId,combination):
	data = {"server":"product_center","url":"/rpc/new_product_lib","interface":"pdt_sku_query","subInterface":"sku_option_combination_get","info":{"productId":productId,"combination":combination}}
	headers = {"Content-Type":"application/json;charset=UTF-8"}
	url = 'http://evaadmin.huishoubao.com/'
	respone = session_public_Amc_login().post(url, headers = headers, json=data, proxies=hsb_eva_ipProxy_test())
	respone.encoding = respone.apparent_encoding  # 编码设置

	if combination == '0':
		# print('响应成功，json格式数据为：\n', respone.text)
		product_options_dict = respone.json()['_data']['options']
		product_aInfo_list = []
		for i in product_options_dict:
			print('SKU选项ID：{0}   SKU选项名称：{1}'.format(i['qId'],i['qName']))
			print(i['aInfo'])
	else:
		# print('响应成功，json格式数据为：\n', respone.text)
		product_combination_dict = respone.json()['_data']['combination']
		for i in product_combination_dict:
			if i['valid'] == '1':
				print('有效组合SKU的答案项aIdList：{0} | fullSkuId：{1} | skuId：{2} | 批发价tradePrice：{3}'.format(
					i['aIdList'],i['fullSkuId'], i['skuId'], i['tradePrice']))

if __name__ == '__main__':
	'''期望：购买渠道 | 存储容量 | 机身内存 | 保修期 | 制式 | 型号 | 颜色'''
	# combination='0'，不获取sku组合的标记
	# sku_option_combination_get(productId='41567',combination='0')
	# sku_option_combination_get(productId='63330',combination='0')
	# sku_option_combination_get(productId='63329',combination='0')
	# sku_option_combination_get(productId='63328',combination='0')
	# sku_option_combination_get(productId='54791',combination='0')
	# sku_option_combination_get(productId='54790',combination='0')
	# sku_option_combination_get(productId='54789',combination='0')
	# sku_option_combination_get(productId='38201',combination='0')
	# sku_option_combination_get(productId='38200',combination='0')
	# sku_option_combination_get(productId='30835',combination='0')
	# sku_option_combination_get(productId='30832',combination='0')
	# sku_option_combination_get(productId='30831',combination='0')
	# sku_option_combination_get(productId='64000',combination='0')  # 华为 P40（5G）
	# sku_option_combination_get(productId='64283',combination='0')
	# sku_option_combination_get(productId='64188',combination='0')
	# sku_option_combination_get(productId='2068',combination='0')
	# sku_option_combination_get(productId='3',combination='0')
	# sku_option_combination_get(productId='1',combination='0')
	# sku_option_combination_get(productId='64001',combination='0')

	# combination='1'，获取sku组合的标记
	sku_option_combination_get(productId='41567',combination='1')
	# sku_option_combination_get(productId='63330',combination='1')
	# sku_option_combination_get(productId='63329',combination='1')
	# sku_option_combination_get(productId='63328',combination='1')
	# sku_option_combination_get(productId='54791',combination='1')
	# sku_option_combination_get(productId='54790',combination='1')
	# sku_option_combination_get(productId='54789',combination='1')
	# sku_option_combination_get(productId='38201',combination='1')
	# sku_option_combination_get(productId='38200',combination='1')
	# sku_option_combination_get(productId='30835',combination='1')
	# sku_option_combination_get(productId='30832',combination='1')
	# sku_option_combination_get(productId='30831',combination='1')
	# sku_option_combination_get(productId='64000',combination='1') # 华为 P40（5G）
	# sku_option_combination_get(productId='64283',combination='1')
	# sku_option_combination_get(productId='64188',combination='1')
	# sku_option_combination_get(productId='2068',combination='1')
	# sku_option_combination_get(productId='3',combination='1')
	# sku_option_combination_get(productId='1',combination='1')
	# sku_option_combination_get(productId='50467',combination='1')
	# sku_option_combination_get(productId='31238',combination='1')

'''SKU选项ID：11   SKU选项名称：购买渠道
[{'aId': '12', 'aName': '大陆国行'}, {'aId': '13', 'aName': '香港行货'}, {'aId': '14', 'aName': '其他国家地区-无锁版'}, {'aId': '15', 'aName': '其他国家地区-有锁版'}, 
 {'aId': '1124', 'aName': '国行官换机/官翻机'}, {'aId': '6047', 'aName': '国行展示机'}, {'aId': '6116', 'aName': '国行BS机'}, {'aId': '7630', 'aName': '监管机'}]
SKU选项ID：122   SKU选项名称：制式
[{'aId': '130', 'aName': '全网通'}, {'aId': '471', 'aName': '移动联通'}]
SKU选项ID：16   SKU选项名称：保修期
[{'aId': '17', 'aName': '剩余保修期大于一个月'}, {'aId': '18', 'aName': '剩余保修期不足一个月或过保'}]
SKU选项ID：2232   SKU选项名称：机身内存
[{'aId': '2235', 'aName': '4GB'}]
SKU选项ID：32   SKU选项名称：存储容量
[{'aId': '36', 'aName': '64GB'}, {'aId': '38', 'aName': '256GB'}, {'aId': '1853', 'aName': '512GB'}]
SKU选项ID：39   SKU选项名称：颜色
[{'aId': '42', 'aName': '银色'}, {'aId': '44', 'aName': '金色'}, {'aId': '1091', 'aName': '深空灰色'}, {'aId': '5566', 'aName': '暗夜绿色'}]
SKU选项ID：918   SKU选项名称：型号
[{'aId': '1083', 'aName': '其他型号'}, {'aId': '6104', 'aName': 'A2217'}]
'''