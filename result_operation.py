#!/usr/bin/env python
# encoding: utf-8
"""
@project:appium_test
@author:cloudy
@site:
@file:result_operation.py
@date:2017/8/25 16:44
"""
import unittest
import requests
import json
import time
import StringIO
from config import DevicesList, DevicesDefault, AppDefault, ProjectName
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

TestResult = unittest.TestResult

class OutputRedirector(object):
    """ Wrapper to redirect stdout or stderr """
    def __init__(self, fp):
        self.fp = fp

    def write(self, s):
        self.fp.write(s)

    def writelines(self, lines):
        self.fp.writelines(lines)

    def flush(self):
        self.fp.flush()

stdout_redirector = OutputRedirector(sys.stdout)
stderr_redirector = OutputRedirector(sys.stderr)


class _TestResult(TestResult):
    # note: _TestResult is a pure representation of results.
    # It lacks the output and reporting ability compares to unittest._TextTestResult.

    def __init__(self, verbosity=1):
        TestResult.__init__(self)
        self.stdout0 = None
        self.stderr0 = None
        self.success_count = 0
        self.failure_count = 0
        self.error_count = 0
        self.verbosity = verbosity

        # result is a list of result in 4 tuple
        # (
        #   result code (0: success; 1: fail; 2: error),
        #   TestCase object,
        #   Test output (byte string),
        #   stack trace,
        # )
        self.result = []
        self.success = []
        #增加一个测试通过率 --Findyou
        self.passrate=float(0)


    def startTest(self, test):
        TestResult.startTest(self, test)
        # just one buffer for both stdout and stderr
        self.outputBuffer = StringIO.StringIO()
        stdout_redirector.fp = self.outputBuffer
        stderr_redirector.fp = self.outputBuffer
        self.stdout0 = sys.stdout
        self.stderr0 = sys.stderr
        sys.stdout = stdout_redirector
        sys.stderr = stderr_redirector


    def complete_output(self):
        """
        Disconnect output redirection and return buffer.
        Safe to call multiple times.
        """
        if self.stdout0:
            sys.stdout = self.stdout0
            sys.stderr = self.stderr0
            self.stdout0 = None
            self.stderr0 = None
        return self.outputBuffer.getvalue()


    def stopTest(self, test):
        # Usually one of addSuccess, addError or addFailure would have been called.
        # But there are some path in unittest that would bypass this.
        # We must disconnect stdout in stopTest(), which is guaranteed to be called.
        self.complete_output()


    def addSuccess(self, test):
        self.success_count += 1
        TestResult.addSuccess(self, test)
        output = self.complete_output()
        self.result.append((0, test, output, ''))
        self.success.append((0, test, output, ''))
        if self.verbosity > 1:
            sys.stderr.write('ok ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('.')

    def addError(self, test, err):
        self.error_count += 1
        TestResult.addError(self, test, err)
        _, _exc_str = self.errors[-1]
        output = self.complete_output()
        self.result.append((2, test, output, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('E  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('E')

    def addFailure(self, test, err):
        self.failure_count += 1
        TestResult.addFailure(self, test, err)
        _, _exc_str = self.failures[-1]
        output = self.complete_output()
        self.result.append((1, test, output, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('F  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('F')


def RunTest(test, verbosity=1):
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    result = _TestResult(verbosity)
    test(result)
    end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    result_operation(result,
                     ProjectName,
                     ProjectName,
                     start_time,
                     end_time,
                     DevicesList[DevicesDefault]['platformName'],
                     DevicesList[DevicesDefault]['platformVersion'],
                     AppDefault
                     )


def result_operation(result,project_name,test_name,start_time,end_time,system,system_version,version):
    """
    测试结果上报
    :param result: 测试结果
    :param project_name: 项目名称
    :param test_name: 测试名称
    :param start_time: 开始时间
    :param end_time: 结束时间
    :param system: 系统
    :param system_version:系统版本
    :param version: 被测版本
    :return:
    """
    server_url = "http://localhost:8888/"
    login_url = server_url + "login"
    username = "auto_test"
    password = "auto_test"
    try:
        session = requests.Session()
        response = session.post(login_url, json.dumps({'username': username, "password": password}))
        if response.status_code == 200:
            ok, test_id = create_test(result, server_url, session, project_name, test_name, start_time, end_time, system, system_version, version)
            if ok:
                test_line_url = server_url + "test/line"
                # 上传失败的测试用例
                upload_failure_case(test_id, test_line_url, session, result.failures)
                # 上传错误的测试用例
                upload_error_case(test_id, test_line_url, session, result.errors)
                # 上传跳过的测试用例
                upload_skip_case(test_id, test_line_url, session, result.skipped)
                # 上传通过的测试用例
                upload_success_case(test_id, test_line_url, session, result.success)
        else:
            print "登录失败，测试结果无法上报"
            return
    except Exception, e:
        print e


def upload_success_case(test_id, base_url, session, success_list=[]):
    """
    上报通过的用例
    :param test_id:
    :param base_url:
    :param session:
    :param success_list:
    :return:
    """
    for i,case_obj, err_info,j in success_list:
        case_name = case_obj._testMethodName
        case_desc = case_obj._testMethodDoc
        desc_tuple = case_desc.split("|")
        case_category = ""
        case_module = ""
        case_function = ""
        if len(desc_tuple) >= 3:
            case_category = desc_tuple[0]
            case_module = desc_tuple[1]
            case_function = desc_tuple[2]
        elif len(desc_tuple) == 2:
            case_module = desc_tuple[0]
            case_function = desc_tuple[1]
        elif len(desc_tuple) == 1:
            case_function = desc_tuple[0]
        data = {
            "Category": case_category,
            "Module": case_module,
            "Function": case_function,
            "Name": case_name,
            "ResultInfo": err_info,
            "Result": "success",
            "Test": test_id

        }
        upload_case_info(base_url, session, data)


def upload_skip_case(test_id, base_url, session, skip_list=[]):
    """
    上报跳过的用例
    :param test_id:
    :param base_url:
    :param session:
    :param skip_list:
    :return:
    """
    for case_obj, err_info in skip_list:
        case_name = case_obj._testMethodName
        case_desc = case_obj._testMethodDoc
        desc_tuple = case_desc.split("|")
        case_category = ""
        case_module = ""
        case_function = ""
        if len(desc_tuple) >= 3:
            case_category = desc_tuple[0]
            case_module = desc_tuple[1]
            case_function = desc_tuple[2]
        elif len(desc_tuple) == 2:
            case_module = desc_tuple[0]
            case_function = desc_tuple[1]
        elif len(desc_tuple) == 1:
            case_function = desc_tuple[0]
        data = {
            "Category": case_category,
            "Module": case_module,
            "Function": case_function,
            "Name": case_name,
            "ResultInfo": err_info,
            "Result": "skip",
            "Test": test_id

        }
        upload_case_info(base_url, session, data)


def upload_error_case(test_id, base_url, session, error_list=[]):
    """
    上报错误的用例
    :param test_id:
    :param base_url:
    :param session:
    :param error_list:
    :return:
    """
    for case_obj, err_info in error_list:
        case_name = case_obj._testMethodName
        case_desc = case_obj._testMethodDoc
        desc_tuple = case_desc.split("|")
        case_category = ""
        case_module = ""
        case_function = ""
        if len(desc_tuple) >= 3:
            case_category = desc_tuple[0]
            case_module = desc_tuple[1]
            case_function = desc_tuple[2]
        elif len(desc_tuple) == 2:
            case_module = desc_tuple[0]
            case_function = desc_tuple[1]
        elif len(desc_tuple) == 1:
            case_function = desc_tuple[0]
        data = {
            "Category": case_category,
            "Module": case_module,
            "Function": case_function,
            "Name": case_name,
            "ResultInfo": err_info,
            "Result": "error",
            "Test": test_id

        }
        upload_case_info(base_url, session, data)


def upload_failure_case(test_id, base_url, session, failure_list=[]):
    """
    上报失败的用例
    :param test_id:
    :param base_url:
    :param session:
    :param failure_list:
    :return:
    """
    for case_obj, err_info in failure_list:
        case_name = case_obj._testMethodName
        case_desc = case_obj._testMethodDoc
        desc_tuple = case_desc.split("|")
        case_category = ""
        case_module = ""
        case_function = ""
        if len(desc_tuple) >= 3:
            case_category = desc_tuple[0]
            case_module = desc_tuple[1]
            case_function = desc_tuple[2]
        elif len(desc_tuple) == 2:
            case_module = desc_tuple[0]
            case_function = desc_tuple[1]
        elif len(desc_tuple) == 1:
            case_function = desc_tuple[0]
        data = {
            "Category": case_category,
            "Module": case_module,
            "Function": case_function,
            "Name": case_name,
            "ResultInfo": err_info,
            "Result": "failure",
            "Test": test_id

        }
        upload_case_info(base_url, session, data)



def upload_case_info(base_url,session,data={}):
    """
    上报测试用例信息
    :param base_url:
    :param session:
    :param data:
    :return:
    """
    response = session.post(base_url, json.dumps(data))
    print response.text


def create_test(result, base_url, session, project_name, test_name, start_time, end_time, system, system_version, version):
    """
    创建测试
    :param result: 测试结果
    :param base_url: 测试上报基地址
    :param session: request session
    :param project_name: 项目名称
    :param test_name: 测试名称
    :param start_time: 开始时间
    :param end_time: 结束时间
    :param system: 系统
    :param system_version:系统版本
    :param version: 被测版本
    :return:
    """
    test_url = base_url + "test"

    failure_count = len(result.failures)
    error_count = len(result.errors)
    skip_count = len(result.skipped)
    success_count = len(result.success)
    data = json.dumps({
        "Name": test_name,
        "StartTime": start_time,
        "EndTime": end_time,
        "ProjectName": project_name,
        "System": system,
        "SystemVersion": system_version,
        "Version": version,
        "SuccessCount": success_count,
        "FailureCount": failure_count,
        "ErrorCount": error_count,
        "SkipCount": skip_count
    })
    response = session.post(test_url, data)
    # 查看返回信息，debug时使用，或者查看错误
    print response.text
    if response.status_code == 200:
        data = json.loads(response.text)
        if data['code'] == 'success':
            return True, data['test']

    return False, 0
if __name__ == "__main__":
    result_operation([], u"珠宝图鉴", u"测试1", "2018-08-12 12:25:23", "2018-08-12 12:25:23", "Android", "4.4.4", "1.2.6")
