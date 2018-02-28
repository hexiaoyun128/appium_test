#!/usr/bin/env python
# encoding: utf-8
"""
@project:appium_test
@author:cloudy
@site:
@file:test_sequence.py
@date:2017/8/25 13:56
"""
import test_case

# 登录测试必须放在最前面
TEST_SEQUENCE = [
    test_case.Login,
    test_case.CompanyManage,
    test_case.Home

]
