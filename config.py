#!/usr/bin/env python
# encoding: utf-8
"""
@project:appium_test
@author:cloudy
@site:
@file:config.py
@date:2017/8/24 11:54
"""
# 项目名称
ProjectName = u"珠宝图鉴"
# 是否开启批量测试
BatchTest = True
# 是否重置应用状态
Reset = True
# 机器列表
DevicesList = {
    "meilan": {
        "deviceName": "810SBN6HBTW9",
        "platformName": "Android",
        "automationName": "Selendroid",
        "platformVersion": "5.1",
        "unicodeKeyboard": True,
        "resetKeyBoard": True,
        "noReset": True,
    },
    "huawei": {
        "deviceName": "8c34fd6fdc93",
        "platformName": "Android",
        "automationName": "Selendroid",
        "platformVersion": "4.4.4",
        "unicodeKeyboard": True,
        "resetKeyBoard": True,
        "noReset": True,
    },
    "127.0.0.1:62001": {
        "deviceName": "8c34fd6fdc93",
        "platformName": "Android",
        "automationName": "Selendroid",
        "platformVersion": "4.4.2",
        "unicodeKeyboard": True,
        "resetKeyBoard": True,
        "noReset": True,
    }
}
# 包名
appPackage = "com.batar.productlibrary"
# 启动类
appActivity = "com.batar.productlibrary.Control.Start.Widget.StartActivity"
# 默认机器
DevicesDefault = "huawei"
# 默认app版本路径
AppDefault = "app-debug.apk"

username = "0001"
password = "123456"
company = {
    "name": u"测试环境",
    "port": 8120
}

