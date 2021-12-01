#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : android_base_page.py
@Author  : liuzhiming
@Time    : 2021/11/30 14:33
"""

from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.mobileby import By
import time
from appium.common.logger import logger
from appium.webdriver.common.touch_action import TouchAction
from utils.logger import LoggerV2



# 启动app方法，返回driver，单例模式
# 封装公共的  确定 取消  返回 这些基础的操作
# 自动从指定目录安装apk
# 自动卸载apk
# 截图：手机截图，保存到项目指定位置
# 抓app日志
# 录制视频
# 获取应用权限，通讯录，音频，视频等
# 封装adb常用命令
# 命令行启动appium服务，并调用，判断是否存在，不存在则启用，存在则pass
# 钉钉通知：发送文本消息、图片消息、视频消息
# 发送邮件通知：主要为测试报告
# 杀死手机上指定程序的进程。强制关闭monkey
# 异常：app闪退，页面元素加载失败或长时间加载，出现anr，





# 定义寻找元素方法字典
FIND_KEYS = {
    # appium supported locator
    "id": By.ID,    # 元素id和 UIAutomatorView 中该元素的 resource id是一致的
    "xpath": By.XPATH,    # 比较绝对，任何一个元素都可以通过xpath进行定位
    "link_text": By.LINK_TEXT,
    "partial_lin_text": By.PARTIAL_LINK_TEXT,
    "name": By.NAME,    # name跟 UIAutomatorView 中该元素的 Text是一致的，Appium v1.0 已经不建议使用通过name进行定位
    "tag_name": By.TAG_NAME,
    "class": By.CLASS_NAME,   # 需要注意：由于 class name不是唯一的，所以可能存在一个页面上有多个元素具有相同的class name。
    # "accessibility_id": "accessibility_id",    # 暂不支持
    # "android_uiautomator": "android_uiautomator",    # 暂不支持
    "css": By.CSS_SELECTOR

}


def start_appium_server():
    pass


"""
desired_caps = {"platformName": "Android",  # 平台名称
                "platformVersion": "7.1.2",  # 系统版本号
                "deviceName": "127.0.0.1:21503",  # 设备名称。如果是真机，在'设置->关于手机->设备名称'里查看
                "appPackage": "com.hll.phone_recycle",  # apk的包名
                "appActivity": "com.hll.phone_recycle.activity.AppStartActivity",  # activity 名称
                "noRest": "True",
                # 设置下面2个参数解决不能输入中文的问题
                "unicodeKeyboard": "True",
                "resetKeyboard": "True"
                }
"""


def get_apk_driver(romote_addr, desired_caps):
    driver = webdriver.Remote(romote_addr, desired_caps)    # 连接appium
    driver.implicitly_wait(5)
    return driver


class AndroidBasePage:

    def __init__(self, apk_driver, timeout=8):
        self.timeout = timeout
        self.driver = apk_driver
        self.logger = LoggerV2()

    def find_element(self, loc):
        """
        接收一个元组对象，第一个参数为定位方法名，第二个为值，第三个为备注名称，例如("xpath", "value", "登录按钮")
        :param loc: is a tuple, ("key", "value", "remark")
        :return: element
        """
        # 判断loc是否为元组
        if not isinstance(loc, tuple):
            self.logger.error("Error：请传入一个元组对象！")
            return False

        # 判断loc长度是否为3
        if len(loc) != 3:
            self.logger.error("Error：元素对象定义错误，请检查包含元素是否为3！")
            return False

        key = loc[0]
        value = loc[1]
        remark = loc[2]
        elem = None

        # 判断定位方法是否在支持范围内
        if key not in FIND_KEYS.keys():
            self.logger.error("[{}]-此元素定位方法不在支持范围内，请更换定位方法!".format(key))
            return False

        # 尝试进行定位，定位到则返回元素对象，定位不到返回 False
        try:
            WebDriverWait(self.driver, self.timeout, 0.5).until(EC.visibility_of_element_located((FIND_KEYS[key], value)))
            elem = self.driver.find_element(FIND_KEYS[key], value)
            return elem
        except Exception as ec:
            self.logger.error("定位元素出现异常：[{}]".format(repr(ec)))

    def send_key(self, loc, value):
        """输入方法"""
        element = self.find_element(loc)
        if element:
            self.logger.debug("输入数据：【{0}】".format(value))
            element.clear()
            element.send_keys(value)

    def click(self, loc):
        """
        点击元素
        :param loc:
        :return:
        """
        element = self.find_element(loc)
        if element:
            self.logger.debug("点击〖{}〗：【{}】>>【{}】".format(loc[2], loc[0], loc[1]))
            element.click()

    def get_elem_text(self, loc):
        """
        获取元素文本信息
        :param loc:
        :return:
        """
        element = self.find_element(loc)
        if element:
            text = element.text
            self.logger.debug("获取到的文本为：【{0}】".format(text))
            return text

    def tap(self, x, y):
        """点击坐标"""
        TouchAction(self.driver).tap(x=x, y=y).perform()

    def press_move_to(self, press, move_to):
        """
        从A坐标点滑动到B坐标
        :param press: 压力点，(x, y)
        :param move_to: 移动点，(x, y)
        :return:
        """
        TouchAction(self.driver).press(x=press[0], y=press[1]).move_to(x=move_to[0], y=move_to[1]).release().perform()
        self.logger.debug("滑动：从{}滑动到{}".format(press, move_to))

    def get_window_size(self):
        """
        获取屏幕尺寸
        :return:
        """
        size = self.driver.get_window_size()
        self.logger.info("屏幕size：宽-{}，高-{}".format(size["width"], size["height"]))
        return size

    def swipe_up(self, t=500, n=1):
        """
        向上滑动屏幕
        :param t: 滑动时间，单位ms
        :param n: 滑动次数
        :return:
        """
        l = self.driver.get_window_size()
        x1 = l['width'] * 0.5     # x坐标
        y1 = l['height'] * 0.75   # 起始y坐标
        y2 = l['height'] * 0.25   # 终点y坐标
        for i in range(n):
            self.driver.swipe(x1, y1, x1, y2, t)

    def swipe_down(self, t=500, n=1):
        """
        向下滑动屏幕
        :param t: 滑动时间，单位ms
        :param n: 滑动次数
        :return:
        """
        l = self.driver.get_window_size()
        x1 = l['width'] * 0.5          # x坐标
        y1 = l['height'] * 0.25        # 起始y坐标
        y2 = l['height'] * 0.75         # 终点y坐标
        for i in range(n):
            self.driver.swipe(x1, y1, x1, y2,t)

    def swip_left(self, t=500, n=1):
        """
        向左滑动屏幕
        :param t:
        :param n:
        :return:
        """
        l = self.driver.get_window_size()
        x1 = l['width'] * 0.75
        y1 = l['height'] * 0.5
        x2 = l['width'] * 0.25
        for i in range(n):
            self.driver.swipe(x1, y1, x2, y1, t)

    def swip_right(self, t=500, n=1):
        """
        向右滑动屏幕
        :param t:
        :param n:
        :return:
        """
        l = self.driver.get_window_size()
        x1 = l['width'] * 0.25
        y1 = l['height'] * 0.5
        x2 = l['width'] * 0.75
        for i in range(n):
            self.driver.swipe(x1, y1, x2, y1, t)

    def scroll_page(self, loc1, loc2, t=2000):
        """
        从一个元素滚动到另一个元素
        :param loc1:
        :param loc2:
        :param t: 滚动时间，单位ms
        :return:
        """
        start_element = self.find_element(loc1)
        stop_element = self.find_element(loc2)
        self.driver.scroll(start_element, stop_element, t)

    def gesture_password(self, pwd, class_name):
        """
        传入九宫格各个数字的class_name(一般情况下，每个数字的class都会相同)，获取到一个元素list
        :param pwd: 手势密码，如5689
        :param class_name:
        :return:
        """
        # 如注册场景需要重复输入手势密码，则调用两次即可
        try:
            list_pwd = self.driver.find_elements_by_class_name(class_name)
            TouchAction(self.driver).press(list_pwd[int(pwd[0])]).move_to(list_pwd[int(pwd[1])]).move_to(
                list_pwd[int(pwd[2])]).wait(100).move_to(
                list_pwd[int(pwd[3])]).wait(100).move_to(list_pwd[8]).release().perform()
            time.sleep(1)
            self.logger.debug("输入手势密码:{}".format(pwd))
            return True
        except Exception as ec:
            self.logger.error("手势密码模拟出现异常：{}".format(repr(ec)))
            return False




