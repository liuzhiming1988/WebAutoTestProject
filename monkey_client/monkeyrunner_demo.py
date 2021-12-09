#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : monkeyrunner_demo.py
@Author  : liuzhiming
@Time    : 2021/12/3 15:02
"""

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage

# 连接手机设备
#参数1：超时时间，单位秒，浮点数。默认是无限期地等待。
#参数2：串deviceid，指定的设备名称。默认为当前设备（手机优先，比如手机通过USB线连接到PC、其次为模拟器）
# device = MonkeyRunner.waitForConnection()   # 默认连接
device = MonkeyRunner.waitForConnection(50.0, "127.0.0.1:21503")   # 参数连接38f782c13b94cc20

# adb获取设备ID
# adb  shell settings get secure android_id

# 截图
result = device.takeSnapshot()
# 将截图保存到文件
result.writeToFile("Test_001.png", "png")   # 当前目录
result.writeToFile("D:\\Test_002.png", "png")
result.writeToFile("..\\Test_003.png", "png")   # 上级目录
result.writeToFile("/Test_004.png", "png")   # 根目录mac、linux,win下为当前盘符的根目录

# 卸载APP
# device.removePackage('cn.richinfo.thinkdrive')
# print ('Uninstall Success!')

# 暂停5秒
# MonkeyRunner.sleep(5)

# 安装新的APP
#以下两种方式都是对的
# device.installPackage('E:/JAVA/monkeyrunner/Test1/ThinkDrive_new.apk')
# device.installPackage('E:\\JAVA\\monkeyrunner\\Test1\\ThinkDrive_new.apk')
#参数可以为绝对路径，也可为相对路径
# print ('Install Success!')

# 卸载设备或模拟器中的APK
#参数为APK包名
# device.removePackage('cn.richinfo.thinkdrive')

# 启动任意的Activity
#device.startActivity(component="包名/启动Activity")
#以下两种都OK
device.startActivity(component="com.hll.phone_recycle/com.hsb.recycle.main.MainActivity")
# device.startActivity(component="cn.richinfo.thinkdrive/.ui.activities.NavigateActivity")
print("start app success")

MonkeyRunner.sleep(8)

#字符串发送到键盘
# device.type('hongge')

#锁屏后,屏幕关闭，可以用下命令唤醒
# device.wake()

# 重启手机
# device.reboot()
# print("reboot phone")

# 模拟滑动
#device.drag(X,Y,D,S)
#X 开始坐标
#Y 结束坐标
#D 拖动持续时间(以秒为单位)，默认1.0秒
#S 插值点时要采取的步骤。默认值是10
# device.drag((100,1053),(520,1053),0.1,10)

#device.touch(x,y,触摸事件类型)
#x,y的单位为像素
#触摸事件类型，请见下文中Findyou对device.press描述
# device.touch(520,520,'DOWN_AND_UP')

"""
1 #device.press(参数1:键码,参数2:触摸事件类型)
 2 #参数1：见android.view.KeyEvent
 3 #参数2，如有TouchPressType()返回的类型－触摸事件类型，有三种。
 4 #1、DOWN 发送一个DOWN事件。指定DOWN事件类型发送到设备，对应的按一个键或触摸屏幕上。
 5 #2、UP 发送一个UP事件。指定UP事件类型发送到设备，对应释放一个键或从屏幕上抬起。
 6 #3、DOWN_AND_UP 发送一个DOWN事件，然后一个UP事件。对应于输入键或点击屏幕。
 7 以上三种事件做为press()参数或touch()参数
 8 
 9 #按下HOME键
10 device.press('KEYCODE_HOME',MonkeyDevice.DOWN_AND_UP) 
11 #按下BACK键
12 device.press('KEYCODE_BACK',MonkeyDevice.DOWN_AND_UP) 
13 #按下下导航键
14 device.press('KEYCODE_DPAD_DOWN',MonkeyDevice.DOWN_AND_UP) 
15 #按下上导航键
16 device.press('KEYCODE_DPAD_UP',MonkeyDevice.DOWN_AND_UP) 
17 #按下OK键
18 device.press('KEYCODE_DPAD_CENTER',MonkeyDevice.DOWN_AND_UP) 
"""


# 在monkeyrunner目录下执行命令
# monkeyrunner [文件路径.py]