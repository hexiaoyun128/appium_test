#!/usr/bin/env python
# encoding: utf-8
"""
@project:appium_test
@author:cloudy
@site:
@file:home.py
@date:2017/8/30 14:08
"""
import unittest
import random
from time import sleep
from BaseTestCase import BaseTestCase
import sys
sys.path.append("..")
import config
from PO import HomePage


# 首页
class Home(BaseTestCase):

    @unittest.skipUnless(config.BatchTest, u"未完成")
    def test_home_001(self):
        u"""大纲测试点:|公司管理|首页轮播左滑"""
        home = HomePage(self.driver)
        home.bottom_go_home_page()
        # 获得轮播的数量
        number = home.get_carousel_number()
        for i in range(number):
            home.carousel_swipe(True)
        self.assertTrue(True, u"测试通过")

    @unittest.skipUnless(config.BatchTest, u"未完成")
    def test_home_002(self):
        u"""大纲测试点:|公司管理|首页轮播右滑"""
        home = HomePage(self.driver)
        home.bottom_go_home_page()
        # 获得轮播的数量
        number = home.get_carousel_number()
        for i in range(number):
            home.carousel_swipe(False)
        self.assertTrue(True, u"测试通过")

    @unittest.skipUnless(config.BatchTest, u"未完成")
    def test_home_003(self):
        u"""大纲测试点:|公司管理|首页轮播随机滑"""
        home = HomePage(self.driver)
        home.bottom_go_home_page()
        # 获得轮播的数量
        number = home.get_carousel_number()
        for i in range(number):
            home.carousel_swipe(random.randint(0,99)/2)
        self.assertTrue(True, u"测试通过")

    @unittest.skipUnless(config.BatchTest, u"未完成")
    def test_home_004(self):
        u"""大纲测试点:|公司管理|首页轮播可点击"""
        home = HomePage(self.driver)
        home.bottom_go_home_page()
        # 获得轮播的数量
        number = home.get_carousel_number()
        for i in range(number):
            home.carousel_swipe(True)
            # 点击轮播图片
            home.carousel_img_click()
            sleep(5)
            home.carousel_img_link_back()
        self.assertTrue(True, u"测试通过")

    @unittest.skipUnless(config.BatchTest, u"未完成")
    def test_home_005(self):
        u"""大纲测试点:|公司管理|快捷推广滑动"""
        home = HomePage(self.driver)
        home.fast_link_swipe(True)
        home.fast_link_swipe(False)

    @unittest.skipUnless(config.BatchTest, u"未完成")
    def test_home_006(self):
        u"""大纲测试点:|公司管理|快捷推广点击"""
        home = HomePage(self.driver)
        home.fast_link_swipe(True)
        home.fast_link_swipe(False)


