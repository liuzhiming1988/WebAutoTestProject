#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : faker_temp.py
@Author  : liuzhiming
@Time    : 2021/11/4 11:52
"""

import faker


class FakerTemp:

    def __init__(self):
        self.f = faker.Faker(locale="zh-CN")
        # 关于初始化参数locale：为生成数据的文化选项，默认为en_US，只有使用了相关文化，才能生成相对应的随机信息（比如：名字，地址，邮编，城市，省份等）

    def get(self):
        print(self.f.name())


"""
country()：国家
province()：省份
city_suffix()：市，县
district()：区
street_address()：街道地址
street_name()：街道名
street_suffix()：街、路
country_code()：国家编码
postcode()：邮编
geo_coordinate()：地理坐标
longitude()：经度
latitude()：纬度
lexify()：替换所有问号？带有随机事件
numerify()：生成三位随机数
random_digit()：生成0~9随机数
random_digit_not_null()：生成1~9的随机数
random_element()：生成随机字母
random_int()：随机数字，默认0~9999，可通过min,max参数修改
random_letter()：随机字母
random_number()：随机数字，参数digits设置生成的数字位数
color_name()：随机颜色名
hex_color()：随机HEX颜色
rgb_color()：随机RGB颜色
safe_color_name()：随机安全色名
safe_hex_color()：随机安全HEX颜色
bs()：随机公司服务名
company()：随机公司名（长）
company_prefix()：随机公司名（短）
company_suffix()：公司性质
credit_card_expire()：随机信用卡到期日
credit_card_full()：生成完整信用卡信息
credit_card_number()：信用卡号
credit_card_provider()：信用卡类型
credit_card_security_code()：信用卡安全码
currency_code()：货币编码
am_pm()：AM/PM
century()：随机世纪
date()：随机日期
date_between()：随机生成指定范围内日期，参数：start_date，end_date
date_between_dates()：随机生成指定范围内日期，用法同上
date_object()：随机生产从1970-1-1到指定日期的随机日期。
date_this_month()：
date_this_year()：
date_time()：随机生成指定时间（1970年1月1日至今）
date_time_ad()：生成公元1年到现在的随机时间
date_time_between()：用法同dates
future_date()：未来日期
future_datetime()：未来时间
month()：随机月份
month_name()：随机月份（英文）
past_date()：随机生成已经过去的日期
past_datetime()：随机生成已经过去的时间
time()：随机24小时时间
timedelta()：随机获取时间差
time_object()：随机24小时时间，time对象
time_series()：随机TimeSeries对象
timezone()：随机时区
unix_time()：随机Unix时间
year()：随机年份
file_extension()：随机文件扩展名
file_name()：随机文件名（包含扩展名，不包含路径）
file_path()：随机文件路径（包含文件名，扩展名）
mime_type()：随机mime Type
ascii_company_email()：随机ASCII公司邮箱名
ascii_email()：随机ASCII邮箱
ascii_free_email()：
ascii_safe_email()：
company_email()：
domain_name()：生成域名
domain_word()：域词(即，不包含后缀)
email()：
free_email()：
free_email_domain()：
f.safe_email()：安全邮箱
f.image_url()：随机URL地址
ipv4()：随机IP4地址
ipv6()：随机IP6地址
mac_address()：随机MAC地址
tld()：网址域名后缀
uri()：随机URI地址
uri_extension()：网址文件后缀
uri_page()：网址文件（不包含后缀）
uri_path()：网址文件路径（不包含文件名）
url()：随机URL地址
user_name()：随机用户名
isbn10()：随机ISBN（10位）
isbn13()：随机ISBN（13位）
job()：随机职位
paragraph()：随机生成一个段落
paragraphs()：随机生成多个段落，通过参数nb来控制段落数，返回数组
sentence()：随机生成一句话
sentences()：随机生成多句话，与段落类似
text()：随机生成一篇文章
word()：随机生成词语
words()：随机生成多个词语，用法与段落，句子，类似
binary()：随机生成二进制编码
boolean()：True/False
language_code()：随机生成两位语言编码
locale()：随机生成语言/国际 信息
md5()：随机生成MD5
null_boolean()：NULL/True/False
password()：随机生成密码,可选参数：length：密码长度；special_chars：是否能使用特殊字符；digits：是否包含数字；upper_case：是否包含大写字母；lower_case：是否包含小写字母
sha1()：随机SHA1
sha256()：随机SHA256
uuid4()：随机UUID
first_name()：
first_name_female()：女性名
first_name_male()：男性名
first_romanized_name()：罗马名
last_name()：
last_name_female()：女
last_name_male()：男
last_romanized_name()：
name()：随机生成姓名
name_female()：男性姓名
name_male()：女性姓名
romanized_name()：罗马名
msisdn()：移动台国际用户识别码，即移动用户的ISDN号码
phone_number()：随机生成手机号
phonenumber_prefix()：随机生成手机号段
profile()：随机生成档案信息
simple_profile()：随机生成简单档案信息

ssn()：生成身份证号

chrome()：随机生成Chrome的浏览器user_agent信息

firefox()：随机生成FireFox的浏览器user_agent信息

internet_explorer()：随机生成IE的浏览器user_agent信息

opera()：随机生成Opera的浏览器user_agent信息

safari()：随机生成Safari的浏览器user_agent信息

linux_platform_token()：随机Linux信息

user_agent()：随机user_agent信息
"""
if __name__ == '__main__':
    f = FakerTemp()
    f.get()

    en = faker.Faker(locale="en_US")
    print(en.phone_number())
