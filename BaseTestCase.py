#!/usr/bin/env python
# encoding: utf-8
"""
@project:appium_test
@author:cloudy
@site:
@file:BaseTestCase.py
@date:2017/8/24 13:47
"""

import os
import unittest
from appium import webdriver
from config import DevicesList,DevicesDefault,AppDefault
from PO import LoginPage
import sys
from time import sleep
sys.path.append("..")
import config
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


# 基础测试类
class BaseTestCase(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['deviceName'] = DevicesList[DevicesDefault]['deviceName']
        desired_caps['platformName'] = DevicesList[DevicesDefault]['platformName']
        desired_caps['platformVersion'] = DevicesList[DevicesDefault]['platformVersion']
        desired_caps['unicodeKeyboard'] = DevicesList[DevicesDefault]['unicodeKeyboard']
        desired_caps['resetKeyBoard'] = DevicesList[DevicesDefault]['resetKeyBoard']
        desired_caps['appPackage'] = config.appPackage
        desired_caps['appActivity'] = config.appActivity
        # desired_caps["automationName"] = DevicesList[DevicesDefault]['automationName']
        if not config.Reset:
            desired_caps["noReset"] = DevicesList[DevicesDefault]['noReset']
        desired_caps['app'] = PATH("apps/android/"+AppDefault)
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

        LoginPage(self.driver).user_login()

    def tearDown(self):
        self.driver.quit()


