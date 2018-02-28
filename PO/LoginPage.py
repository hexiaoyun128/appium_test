#!/usr/bin/env python
# encoding: utf-8
"""
@project:appium_test
@author:cloudy
@site:
@file:LoginPage.py
@date:2017/8/28 13:43
"""
from .Base import Base

import sys
sys.path.append("..")
import config

# 登录页
class LoginPage(Base):

    # 用户信息
    go_user_info_id = "com.batar.productlibrary:id/main_mine_userInfor_into"
    # 用户名
    input_username_id = "com.batar.productlibrary:id/host_customer"
    # 密码
    input_password_id = "com.batar.productlibrary:id/host_customer_password"
    # 登录
    login_confirm_id = "com.batar.productlibrary:id/host_btn_login"
    # 取消登录，返回源页面
    login_cancel_id = "com.batar.productlibrary:id/host_return"
    # 公司
    company_grid_id = "com.batar.productlibrary:id/host_gridview"
    # 记住密码
    remember_pwd_id = "com.batar.productlibrary:id/host_remember_password_button"

    def remember_password(self):
        """
        记住密码
        :return:
        """
        self.driver.find_element_by_id(self.remember_pwd_id).click()

    def go_user_info(self):
        """
        进入用户信息页面，若未登录进入登录页面
        :return:
        """
        self.bottom_go_mine_page()
        self.driver.find_element_by_id(self.go_user_info_id).click()

    def input_login_username(self, username):
        """
        输入用户名
        :param username: 登录用户名
        :return:
        """
        username_input = self.driver.find_element_by_name(self.input_username_id)
        username_input.clear()
        username_input.send_keys("%s" % username)

    def input_login_password(self, password):
        """
        输入登录密码
        :param password: 登录密码
        :return:
        """
        password_input = self.driver.find_element_by_id(self.input_password_id)
        password_input.clear()
        password_input.send_keys("%s" % password)

    def login_confirm(self):
        """
        确认登录
        :return:
        """
        self.driver.find_element_by_id(self.login_confirm_id).click()

    def login_cancel(self):
        """
        取消登录，返回源页面
        :return:
        """
        self.driver.find_element_by_id(self.login_cancel_id).click()

    def add_new_company(self):
        """
        前往增加公司页面
        :return:
        """
        parent_node = self.driver.find_element_by_id(self.company_grid_id)

        nodes = parent_node.find_element_by_class_name("android.widget.FrameLayout")

        add_text = u"添加公司"
        for node in nodes:
            text_node = node.find_element_by_class_name("android.widget.TextView")
            if text_node.text == add_text:
                node.click()
                break

    def user_login(self):
        """
        登录
        :return:
        """
        self.go_user_info()
        self.input_login_username(config.username)
        self.input_login_password(config.password)
        self.login_confirm()




