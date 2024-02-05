# -*- coding: utf-8 -*-
# @Time    : 2023/3/23  11:28
# @Author  : jikkdy
# @FileName: conftest.py
"""
    Description:共享夹具
"""

import pytest
from selenium import webdriver

import settings
from page_objects.login_page import LoginPage

# @pytest.fixture(scope='class')
# def driver():
#     with webdriver.Chrome() as wd:
#         # 最大化游览器
#         wd.maximize_window()
#         # 返回游览器对象，不能使用return，return返回之后会关闭游览器，无法进行后续操作
#         yield wd
@pytest.fixture(scope='class')
def driver(pytestconfig):
    if pytestconfig.getoption('--browser')=='edge':
        with webdriver.Edge(executable_path=settings.BROWSER_DRIVERS['edge']) as wd:
            wd.maximize_window()
            yield wd
    elif pytestconfig.getoption('--browser')=='chrome':
        with webdriver.Edge(executable_path=settings.BROWSER_DRIVERS['chrome']) as wd:
            wd.maximize_window()
            yield wd




# 直接定义登录成功的夹具（一般不使用）
# @pytest.fixture(scope='class')
# def login_driver():
#     with webdriver.Chrome() as wd:
#         # 最大化游览器
#         wd.maximize_window()
#         # 1.登录页面
#         lp=LoginPage(wd)
#         wd.get(lp.settings.PROJECT_HOST+lp.settings.INTERFACE['login'])
#         lp.login(lp.settings.TEST_NORMAL_USERNAME,lp.settings.TEST_NORMAL_PASSWORD)
#         # 返回登录后的游览器驱动
#         yield wd


# 继承原来的夹具，增加登录功能
@pytest.fixture(scope='class')
# 参数名与上面的夹具同名
def logged_in_driver(driver):
    lp=LoginPage(driver)
    driver.get(lp.settings.PROJECT_HOST+lp.settings.INTERFACE['login'])
    lp.login(lp.settings.TEST_NORMAL_USERNAME, lp.settings.TEST_NORMAL_PASSWORD)
    # 返回webdriver
    yield driver


def pytest_addoption(parser):
    # 定义pytest的参数
    parser.addoption("--browser",default='chrome')   # 坑 参数都是--小写