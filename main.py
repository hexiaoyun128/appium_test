#!/usr/bin/env python
# encoding: utf-8
"""
@project:appium_test
@author:cloudy
@site:
@file:main.py
@date:2017/8/22 13:41
"""
import unittest
import doctest

import time
from test_sequence import TEST_SEQUENCE
from result_operation import RunTest,result_operation


suite = doctest.DocTestSuite()
# 用例测试顺序
for test_class in TEST_SEQUENCE:
    suite.addTest(unittest.makeSuite(test_class))
# 上报到服务器
up_server = False
if up_server:
    # 测试结果在对象中

    RunTest(suite, 1)

else:
    # 直接打印结果
    runner = unittest.TextTestRunner()
    runner.run(suite)
