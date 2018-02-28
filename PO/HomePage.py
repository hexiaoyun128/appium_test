#!/usr/bin/env python
# encoding: utf-8
"""
@project:appium_test
@author:cloudy
@site:
@file:HomePage.py
@date:2017/8/28 13:49
"""
from .Base import Base
from appium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait

class HomePage(Base):

    # 轮播按钮
    carousel_btn_id = "com.batar.productlibrary:id/viewpagerIndicatorLayout"
    # 轮播容器
    carousel_id = "com.batar.productlibrary:id/main_CycleViewPager"
    # 轮播图片
    carousel_img_id = "com.batar.productlibrary:id/cycle_img"
    # 轮播图片点击后页面返回按钮id
    carousel_img_link_back_id = "com.batar.productlibrary:id/banner_top_back"
    # 快捷推广
    fast_link_container_id = "com.batar.productlibrary:id/main_HorizontalScrollView"
    # 快捷推广点击
    fast_link_click_class = "android.widget.LinearLayout"

    def carousel_img_link_back(self):
        """
        轮播图片点击后返回
        :return:
        """
        self.driver.find_element_by_id(self.carousel_img_link_back_id).click()

    def carousel_img_click(self):
        """
        轮播图片点击
        :return:
        """
        self.driver.find_element_by_id(self.carousel_img_id).click()

    def get_carousel_number(self):
        """
        获得轮播图片的数量
        :return: 返回轮播图片数量
        """
        container = self.driver.find_element_by_id(self.carousel_btn_id)
        return len(container.find_elements_by_class_name("android.widget.LinearLayout"))

    def carousel_swipe(self, left=True):
        """
        轮播图片滑动
        :param left: 左滑动，否则右滑动
        :return:
        """
        self.element_swipe_vertical(self.carousel_id, left)

    def fast_link_swipe(self, left=True):
        """
        快捷推广滑屏
        :return:
        """
        self.element_swipe_vertical(self.fast_link_container_id, left)
    def fast_link_click(self):
        """
        快捷推广点击
        :return:
        """
        els = self.driver.find_elements_by_class_name(self.fast_link_click_class)
        for el in range(els):
            el.click()




