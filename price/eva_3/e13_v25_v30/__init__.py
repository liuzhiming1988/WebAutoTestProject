# -*- coding: utf-8 -*-
# @File    : __init__.py.py
# @Time    : 2021/8/26 15:21
# @Author  : MikingZhang

'''
/huishoubao/config
vim BasePriceEvaluate.xml

【BasePriceEvaluate】所涉应用已经发到K8S了，要走K8S服务，注意①hosts，②配置文件的更改

1. 销售价方案ID
<Other>
    <Key>DefSalePlanId</Key>
    <Value>3</Value>
</Other>

2. 开启2.5转3.0
<Other>
    <Key>Enable25To3</Key>
    <Value>0</Value>
</Other>
3. 更改之后无需重启服务，最多2分钟起效

用例1：version保留1，销售方案估价，使用类型-34-估价，
    1.1. 销售定价维护，保存一遍机型
    1.2. 开启2.5转3.0
    1.3. channelId='10000837', pid='3413'  一次加成渠道   √
    1.4. channelId='10000837', pid='3415'  二次加成渠道   √

用例2：version切成2，销售方案估价，可以继续使用类型-34，如果同样选项的机型，价格会是一致
    2.1. 销售定价维护，保存一遍机型
    2.2. 开启2.5转3.0
    2.3. channelId='10000837', pid='3413'  一次加成渠道   √
    3.4. channelId='10000837', pid='3415'  二次加成渠道   √
'''