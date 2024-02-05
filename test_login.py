# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
# from test_cases.base_case import BaseCase
#
# # 继承基类
# class TestLogin(BaseCase):
#     name='登录功能'
#
#     # 传入夹具名称driver，pytest自动发现并调用
#     def test_login_success(self,driver):
#         '''测试登录成功'''
#         # 1.访问登录页面
#         driver.get(self.settings.PROJECT_HOST+self.settings.INTERFACE['login'])
#         # 2.输入用户名和密码
#         # 2.1 定位输入框
#         # 定义元素等待时间
#         wait=WebDriverWait(driver,timeout=3)
#         username_input=wait.until(
#             EC.visibility_of_element_located(('xpath','//input[@name="username"]'))
#         )
#         # 2.2 输入用户名
#         username_input.send_keys(self.settings.TEST_NORMAL_USERNAME)
#         # 2.3 定位密码框、输入密码
#         wait.until(
#             EC.visibility_of_element_located(('xpath', '//input[@name="password"]'))
#         ).send_keys(self.settings.TEST_NORMAL_PASSWORD)
#         # 3.输入验证码
#         wait.until(
#             EC.visibility_of_element_located(('xpath', '//input[@name="verify_code"]'))
#         ).send_keys(self.settings.TEST_NORMAL_VERIFY)
#         # 4.点击登录
#         wait.until(
#             EC.visibility_of_element_located(('xpath', '//a[@name="sbtbutton"]'))
#         ).click()
#         # 5.断言是否登录成功
#         # 断言标准怎么简单怎么来，怎么可靠怎么来，没有固定的模式，要灵活
#         # 本案例中，就是判断是否出现退出按钮
#         assert wait.until(EC.visibility_of_element_located(('xpath','//a[@title="退出"]')))



# from page_objects.login_page import LoginPage
# from page_objects.home_page import HomePage
# from test_cases.base_case import BaseCase
#
# class TestLogin(BaseCase):
#     name='登录功能'
#
#     # 调用名为driver的夹具
#     def test_login(self,driver):
#         # 测试登录功能
#
#         # 实例化登录页面
#         lp=LoginPage(driver)
#         # 调用登录方法
#         # lp.login(self.settings.TEST_NORMAL_USERNAME,self.settings.TEST_NORMAL_PASSWORD,self.settings.TEST_NORMAL_VERIFY)
#         lp.login(self.settings.TEST_NORMAL_USERNAME,self.settings.TEST_NORMAL_PASSWORD)
#         # 断言
#         hp=HomePage(driver)
#         assert hp.get_logout_btn()




# 五、登录功能测试

import pytest

import settings
from page_objects.login_page import LoginPage
from page_objects.home_page import HomePage
from test_cases.base_case import BaseCase
from test_data.login_data import success_cases,fail_cases,error_cases

import pytest
pytestmark = pytest.mark.mark_name
# 或者多个标记
# pytestmark = [pytest.mark.mark_name1, pytest.mark.mark_name2]


@pytest.mark.login
class TestLogin(BaseCase):
    name='登录功能'

    @pytest.mark.success
    # 数据参数化，case为数据参数名，success_cases为传入的数据
    @pytest.mark.parametrize('case',success_cases)
    def test_login_success(self,driver,case):
        '''
        登录页面的登录功能
        :param username: 用户名
        :param password: 密码
        :param remember: 是否记住账号密码
        :return:
        '''
        self.logger.info('***{}用例开始测试***'.format(case['title']))
        # 1.打开登录页面
        driver.get(self.settings.PROJECT_HOST+settings.INTERFACE['login'])
        # 2.登录
        lp=LoginPage(driver)
        lp.login(**case['request_data'])
        # 3.断言是否登录成功
        hp=HomePage(driver)
        assert hp.get_logout_btn()
        # 4.退出
        hp.logout()
        # 5.再访问登录页面
        driver.get(self.settings.PROJECT_HOST + settings.INTERFACE['login'])
        # 6.断言账号密码是否有保存
        try:
            if case['request_data']['remember']:
                # 断言登录信息是否有保存
                assert lp.get_user_value()==case['request_data']['username']
            else:
                # 断言手机号码没有保存
                assert not lp.get_user_value()
        except Exception as e:
            self.logger.exception('断言失败')
            raise e
        else:
            self.logger.info('***{}用例通过测试***'.format(case['title']))
        self.logger.info('***{}用例结束测试***'.format(case['title']))

    @pytest.mark.parametrize('case',fail_cases)
    def test_login_fail(self,case,driver):
        '''
        登录失败
        :param case: 用例数据
        :param driver: 夹具信息
        :return:
        '''
        self.logger.info('***{}用例开始测试***'.format(case['title']))
        # 1.打开登录页面
        driver.get(self.settings.PROJECT_HOST+self.settings.INTERFACE['login'])
        # 2.登录
        lp=LoginPage(driver)
        lp.login(**case['request_data'])
        # 3.断言
        try:
            assert case['error_tip']==lp.get_error_tip()
        except Exception as e:
            self.logger.exception('断言失败')
            raise e
        else:
            self.logger.info('***{}用例通过测试***'.format(case['title']))
        self.logger.info('***{}用例结束测试***'.format(case['title']))

    @pytest.mark.parametrize('case',error_cases)
    def test_login_error_username_password(self,driver,case):
        '''
        用户名或密码错误
        :param driver:
        :param case:
        :return:
        '''
        self.logger.info('***{}用例开始测试***'.format(case['title']))
        # 1.打开登录页面
        driver.get(self.settings.PROJECT_HOST + self.settings.INTERFACE['login'])
        # 2.登录
        lp = LoginPage(driver)
        lp.login(**case['request_data'])
        # 3.断言
        try:
            assert case['error_tip'] == lp.get_error_pop_tip()
        except Exception as e:
            self.logger.exception('断言失败')
            raise e
        else:
            self.logger.info('***{}用例通过测试***'.format(case['title']))
        self.logger.info('***{}用例结束测试***'.format(case['title']))


class TestHaa(BaseCase):
    def test_01(self):
        print(1)


