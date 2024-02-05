# -*- coding: utf-8 -*-
# @Time    : 2023/4/3  11:25
# @Author  : jikkdy
# @FileName: test_invest.py
import pytest

from test_cases.base_case import BaseCase
from page_objects.bid_page import BidPage
from page_objects.home_page import HomePage

from test_data.invest_data import success_cases,fail_cases


class TestInvest(BaseCase):
    name = '投资功能'

    @pytest.mark.parametrize('case',success_cases)
    def test_invest_success(self,logged_in_driver,case):
        self.logger.info('***{}用例开始测试***'.format(case['title']))
        # 1.进入首页面
        logged_in_driver.get(self.settings.PROJECT_HOST)
        # 2.选择第一个标
        hp=HomePage(logged_in_driver)
        hp.select_first_bid()
        # 3.获取标的投资前的可投资额
        bp=BidPage(logged_in_driver)
        bid_balance_before_invest=bp.get_bid_balance()
        # 4.获取用户投资前的余额
        user_balance_before_invest = bp.get_user_balance()
        # 5.投资
        bp.invest(**case['request_data'])
        # 6.断言是否弹出投资成功弹出框
        assert bp.get_invest_success_pop()
        # 7.刷新页面
        logged_in_driver.refresh()
        # 8.获取标的投资后的可投资额
        bid_balance_after_invest = bp.get_bid_balance()
        # 9.获取用户投资后的余额
        user_balance_after_invest = bp.get_user_balance()
        try:
            # 10.断言投资前标的可投资额-投资后标的可投资额=投资额
            assert bid_balance_before_invest - bid_balance_after_invest==case['request_data']['amount']
            # 11.断言投资前用户的余额-投资后用户的余额=投资额
            assert user_balance_before_invest - user_balance_after_invest==case['request_data']['amount']
        except Exception as e:
            self.logger.exception('断言失败')
            raise e
        else:
            self.logger.info('***{}用例通过测试***'.format(case['title']))
        self.logger.info('***{}用例结束测试***'.format(case['title']))


    @pytest.mark.parametrize('case',fail_cases)
    def test_invest_fail(self,logged_in_driver,case):
        self.logger.info('***{}用例开始测试***'.format(case['title']))
        # 1.投资
        bid=BidPage(logged_in_driver)
        bid.invest(**case['request_data'])
        # 2.断言错误信息
        try:
            assert case['error_tip']==bid.get_pop_error_tip()
        except Exception as e:
            self.logger.exception('断言失败')
            raise e
        else:
            self.logger.info('***{}用例通过测试***'.format(case['title']))
        self.logger.info('***{}用例结束测试***'.format(case['title']))