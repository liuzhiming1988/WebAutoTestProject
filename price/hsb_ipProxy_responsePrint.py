#!/usr/bin/env python
# -*- coding:utf-8 -*-

# @Author:MikingZhang


import requests
import json

def hsb_amc_ipProxy_test():
    '''1. AMC-vpc测试环境'''
    hsb_amc_ipProxy = {'http':'139.199.211.123'}
    print('\033[31m您调用的是『AMC-vpc测试环境』，HOSTS指向IP为：『{0}』\033[0m'.format(hsb_amc_ipProxy['http']))

    '''2. AMC-pre环境'''
    # hsb_amc_ipProxy = {'http': '42.193.141.154'}
    # print('\033[31m您调用的是『AMC-pre测试环境』，HOSTS指向IP为：『{0}』\033[0m'.format(hsb_amc_ipProxy['http']))
    return hsb_amc_ipProxy

def hsb_eva_ipProxy_test():
    '''1. vpc测试-环境'''
    hsb_eva_ipProxy = {'http':'193.112.170.216'}
    print('\033[31m您调用的是『价格FT-vpc测试环境』，HOSTS指向IP为：『{0}』\033[0m'.format(hsb_eva_ipProxy['http']))

    '''2. vpc测试环境-K8S'''
    # hsb_eva_ipProxy = {'http': '1.14.234.191'}
    # print('\033[31m您调用的是『价格FT-vpc测试环境-K8S』，HOSTS指向IP为：『{0}』\033[0m'.format(hsb_eva_ipProxy['http']))

    '''3. pre环境'''
    # hsb_eva_ipProxy = {'http': '159.75.119.107'}
    # print('\033[31m您调用的是『价格FT-pre环境』，HOSTS指向IP为：『{0}』\033[0m'.format(hsb_eva_ipProxy['http']))

    '''4. 生产环境（压测，临时使用）'''
    # hsb_eva_ipProxy = {'http': '106.55.175.95'}
    # print('\033[31m您调用的是『价格FT-生产环境（压测，临时使用）』，HOSTS指向IP为：『{0}』\033[0m'.format(hsb_eva_ipProxy['http']))
    return hsb_eva_ipProxy

def hsb_eva_ipProxy_k8s_test():
    '''1. 测试K8S环境'''
    hsb_eva_ipProxy_k8s_test = {'http':'159.75.145.158'}
    print('\033[31m您调用的是『价格FT-测试K8S环境』，HOSTS指向IP为：『{0}』\033[0m'.format(hsb_eva_ipProxy_k8s_test['http']))
    return hsb_eva_ipProxy_k8s_test

def hsb_eva_admin_ipProxy_test():
    '''1. hsb-价格，admin.huishoubao.com.cn 测试环境，指向代理hosts'''
    hsb_eva_admin_ipProxy = {'http':'134.175.235.150'}
    print('\033[31m您调用的是『HSB-价格-admin.huishoubao.com.cn-测试环境』，HOSTS指向IP为：『{0}』\033[0m'.format(hsb_eva_admin_ipProxy['http']))

    '''2. hsb-价格，admin.huishoubao.com.cn pre环境，指向代理hosts'''
    # hsb_eva_admin_ipProxy = {'http': '159.75.85.15'}
    # print('\033[31m您调用的是『HSB-价格-admin.huishoubao.com.cn-pre环境』，HOSTS指向IP为：『{0}』\033[0m'.format(hsb_eva_admin_ipProxy['http']))
    return hsb_eva_admin_ipProxy

def hsb_ordserver_ipProxy_test():
    ''' hsb-订单-测试环境，指向代理hosts
        134.175.174.142 bangmai.order.huishoubao.com
        134.175.174.142 ordserver.huishoubao.com '''
    hsb_ordserver_ipProxy_test = {'http':'134.175.174.142'}
    print('\033[31m您调用的是『HSB-order订单服务-测试环境』，HOSTS指向IP为：『{0}』\033[0m'.format(hsb_ordserver_ipProxy_test['http']))
    return hsb_ordserver_ipProxy_test

def hsb_wms_ipProxy_test():
    ''' hsb-WMS-测试环境，指向代理hosts 139.199.211.123'''
    hsb_wms_ipProxy_test = {'http':'139.199.211.123'}
    print('\033[31m您调用的是『HSB-WMS收货系统-测试环境』，HOSTS指向IP为：『{0}』\033[0m'.format(hsb_wms_ipProxy_test['http']))
    return hsb_wms_ipProxy_test

def hsb_apiOMS_ipProxy_test():
    ''' hsb-后端-oms，指向代理hosts'''
    hsb_apiOMS_ipProxy_test = {'http':'139.199.211.123'}
    print('\033[31m您调用的是『HSB-OMS订单系统-测试环境』，HOSTS指向IP为：『{0}』\033[0m'.format(hsb_apiOMS_ipProxy_test['http']))
    return hsb_apiOMS_ipProxy_test

def hsb_api_huishoubao_test():
    ''' hsb-自有，指向代理hosts'''
    hsb_apiHuishoubao_ipProxy_test = {'http':'182.254.197.228'}
    print('\033[31m您调用的是『HSB-自有-测试环境』，HOSTS指向IP为：『{0}』\033[0m'.format(hsb_apiHuishoubao_ipProxy_test['http']))
    return hsb_apiHuishoubao_ipProxy_test

def hsb_channel_api_test():
    ''' hsb-自有，指向代理hosts'''
    hsb_channel_api_ipProxy_test = {'http':'134.175.235.150'}
    print('\033[31m您调用的是『HSB-渠道中心-测试环境』，HOSTS指向IP为：『{0}』\033[0m'.format(hsb_channel_api_ipProxy_test['http']))
    return hsb_channel_api_ipProxy_test

def hsb_sales_JingPai_ipProxy_test():
    '''hsb-销售竞拍-测试环境，指向代理hosts'''
    hsb_sales_JingPai_ipProxy_test = {'http':'118.89.42.94'}
    print('\033[31m您调用的是『HSB-销售竞拍-测试环境』，HOSTS指向IP为：『{0}』\033[0m'.format(hsb_sales_JingPai_ipProxy_test['http']))
    return hsb_sales_JingPai_ipProxy_test

def hsb_eva_ipProxy_on_line():
    '''hsb生产环境，指向代理hosts'''
    hsb_eva_ipProxy_on_line = {'http':'xxxxxxx'}
    print('\033[31m您调用的是『HSB-价格FT-生产环境』，HOSTS指向IP为：『{0}』\033[0m'.format(hsb_eva_ipProxy_on_line['http']))
    return hsb_eva_ipProxy_on_line

def hsb_eva_ipProxy_dev():
    '''hsb-开发环境，指向代理hosts'''
    hsb_eva_ipProxy_dev = {'http':'119.29.8.123'}
    print('\033[31m您调用的是『HSB-价格FT-开发环境』，HOSTS指向IP为：『{0}』\033[0m'.format(hsb_eva_ipProxy_dev['http']))
    return hsb_eva_ipProxy_dev

def hsb_baseprice_ipProxy_test():
    '''hsb-价格-定价系统-测试环境，指向代理hosts'''
    hsb_baseprice_ipProxy_test = {'http':'193.112.170.216'}
    print('\033[31m您调用的是『HSB-定价系统-测试环境』，HOSTS指向IP为：『{0}』\033[0m'.format(hsb_baseprice_ipProxy_test['http']))
    return hsb_baseprice_ipProxy_test

def hsb_hsbpro_ipProxy_test():
    '''hsb-专业版App-测试环境，指向代理hosts'''
    hsb_hsbpro_ipProxy_test = {'http':'106.55.146.198', 'https':'106.55.146.198'}
    print('\033[31m您调用的是『HSB-专业版App-测试环境』，HOSTS指向IP为：『{0}』\033[0m'.format(hsb_hsbpro_ipProxy_test['https']))
    return hsb_hsbpro_ipProxy_test

def hsb_baseprice_ipProxy_dev():
    '''hsb-价格-定价系统-开发环境，指向代理hosts'''
    hsb_baseprice_ipProxy_dev = {'http':'111.230.67.6'}
    print('\033[31m您调用的是『HSB-定价系统-开发环境』，HOSTS指向IP为：『{0}』\033[0m'.format(hsb_baseprice_ipProxy_dev['http']))
    return hsb_baseprice_ipProxy_dev

def hsb_response_print(respone):
    '''响应结果打印输出，方法封装'''
    respone.encoding = respone.apparent_encoding  # 编码设置
    print(json.dumps(respone.json(),indent=4,ensure_ascii=False))
    print('\n==========>接口响应『json』格式数据为：\n', respone.text
        + '\n==========>接口响应时长：{0} 秒\n'.format(respone.elapsed.total_seconds())
        + '\033[32m=\033[0m' * 180
        + '\n')

def miking_print():
    print('\033[32m=\033[0m' * 180)