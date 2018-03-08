#!/usr/bin/env python
# encoding: utf-8
"""
@project:appium_test
@author:cloudy
@site:
@file:Base.py
@date:2017/8/28 13:50
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions


# 基础类
class Base(object):

    driver = None

    def __init__(self, driver):
        self.driver = driver

    def get_screen_size(self):
        """
        获得屏幕尺寸
        :return: （width,height）
        """
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        return x, y

    def get_element_location_by_id(self, element_id):
        """
        获得元素的信息
        :param element_id:
        :return:
        """
        el = self.driver.find_element_by_id(element_id)
        location = el.location
        size = el.size
        return {
            "x": location["x"],
            "y": location["y"],
            "width": size["width"],
            "height": size["height"],
        }

    def exsit_element_by_id(self,element_id):
        """
        判断el是否存在
        :param element_id:
        :return:
        """
        try:
            self.driver.find_element_by_id(element_id)
            return True
        except Exception,e:
            return False

    def element_swipe_vertical(self,element_id="", left=True):
        """
        在element上横向滑屏
        :param element_id: 元素id
        :param left: 向左或者向右
        :return:
        """
        el_info = self.get_element_location_by_id(element_id)
        point_y = el_info["y"] + el_info["height"]/2
        point_x_right = el_info["x"] + el_info["width"] * 0.75
        point_x_left = el_info["x"] + el_info["width"] * 0.25
        if left:
            self.driver.swipe(point_x_right, point_y, point_x_left, point_y)
        else:
            self.driver.swipe(point_x_left, point_y, point_x_right, point_y)

    def element_swipe_horizontal(self, element_id="", up=True):
        """
        在element上垂直滑屏
        :param element_id: 元素id
        :param up: 向上或者向下
        :return:
        """
        el_info = self.get_element_location_by_id(element_id)
        point_x = el_info["x"] + el_info["width"] / 2
        point_y_top = el_info["y"] + el_info["height"] * 0.75
        point_y_bottom = el_info["y"] + el_info["height"] * 0.25

        if up:
            self.driver.swipe(point_x, point_y_top, point_x, point_y_bottom)
        else:
            self.driver.swipe(point_x, point_y_bottom, point_x, point_y_top)


    def load_page_done(self, element_id=""):
        """
        判断页面加载是否完成
        :param element_id:
        :return:
        """
        WebDriverWait(self.driver, 5).until(lambda driver: driver.find_element_by_id(element_id).is_displayed())

    # ===========================首页底部button============================

    def bottom_go_home_page(self):
        """
        到主页
        :return:
        """
        self.driver.find_element_by_id("com.batar.productlibrary:id/main_bottom_home").click()

    def bottom_go_find_page(self):
        """
        到发现页
        :return:
        """
        self.driver.find_element_by_id("com.batar.productlibrary:id/main_bottom_discover").click()

    def bottom_go_shopping_cart_page(self):
        """
        到购物车页
        :return:
        """
        self.driver.find_element_by_id("com.batar.productlibrary:id/main_bottom_shopping").click()

    def bottom_go_mine_page(self):
        """
        到我的图鉴页
        :return:
        """
        self.driver.find_element_by_id("com.batar.productlibrary:id/main_bottom_mine").click()

    # def find_toast(self, message):
    #         u"""判断toast信息"""
    #         try:
    #             element = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.LINK_TEXT, message)))
    #             return True
    #         except Exception:
    #             print Exception.message
    #             return False
    def find_toast(self, message):
            u"""判断toast信息"""
            # message = '//*[@text=u\'{}\']'.format(message)
            try:
                element = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.PARTIAL_LINK_TEXT, message)))
                return True
            except Exception:
                print Exception.message
                return False


