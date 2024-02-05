# -*- coding: utf-8 -*-
# @Time    : 2023/4/13  11:51
# @Author  : jikkdy
# @FileName: test_attend.py
import pytest
from test_cases.base_case import BaseCase

from page_objects.login_page import LoginPage
from page_objects.main_page import MainPage
from page_objects.course_page import CoursePage
from test_data.attend_data import student_list

class TestAttendFlow(BaseCase):
    name = '考勤功能业务流'

    def test_create_number_attendance(self,driver):
        '''
        老师创建数字考勤
        :param driver:
        :return:
        '''
        self.logger.info('--------开始测试老师创建数字考勤----------')
        try:
            # 1.访问登录页面
            driver.get(self.settings.PROJECT_HOST+self.settings.INTERFACE['login'])
            # 2.登录老师账号
            lp=LoginPage(driver)
            lp.login(self.settings.TEST_TEC_USERNAME,self.settings.TEST_TEC_PASSWORD)
            # 3.进入对应课程
            mp=MainPage(driver)
            mp.select_first_teaching_course()
            # 4.点击考勤标签
            # 5.点击新建考勤
            # 6.选择数字考勤
            # 7.点击确定
            # 8.设置考勤时长并确定
            cp=CoursePage(driver)
            title,attend_code=cp.create_number_attendance()

            # 绑定到类属性中共享
            self.__class__.title=title
            self.__class__.attend_code=attend_code
        except Exception as e:
            raise AssertionError('****创建数字考勤失败*****')
        self.logger.info('----创建数字考勤成功，title={}，考勤码={}----'.format(title,attend_code))

    @pytest.mark.parametrize('case',student_list)
    def test_student_attend(self,driver,case):
        '''
        学生登录并签到
        :param driver:
        :param case:
        :return:
        '''
        self.logger.info('------开始测试学生签到数字考勤-------')
        # 1.访问登录页面
        driver.get(self.settings.PROJECT_HOST+self.settings.INTERFACE['login'])
        # 2.登录学生账号
        lp=LoginPage(driver)
        lp.login(**case)
        # 3.进入课程
        mp=MainPage(driver)
        mp.select_first_learning_course()
        # 4.签到
        cp=CoursePage(driver)
        cp.stu_number_attend(self.attend_code)
        cp.delay(3)
        tm,title,res=cp.get_first_attendance_record()
        assert (title,res)==(self.title,'出勤')

        # 绑定考勤人数可以做结束考勤时的检验
        # 获取对象的attend_num属性，若无该属性给attend_num赋值为0
        attend_num=getattr(self,'attend_num',0)
        # 每执行一个用例，attend_num加1
        self.__class__.attend_num=attend_num+1
        self.logger.info('-----签到成功，共签到{}位学生----'.format(attend_num+1))

    def test_close_attendance(self,driver):
        '''
        结束考勤
        :param driver:
        :return:
        '''
        self.logger.info('-----开始测试结束考勤--------')
        # 1.访问登录页面
        driver.get(self.settings.PROJECT_HOST+self.settings['login'])
        # 2.登录老师账号
        lp=LoginPage(driver)
        lp.login(self.settings.TEST_TEC_PASSWORD,self.settings.TEST_TEC_PASSWORD)
        # 3.进入课程
        mp=MainPage(driver)
        mp.select_first_teaching_course()
        # 4.结束考勤
        cp=CoursePage(driver)
        # 有两个返回值，第二个返回值在后续中不使用，故使用_接收
        num,_=cp.close_number_attendance()

        assert num==self.attend_num
        self.logger.info('-----结束考勤测试，共签到{}学生--------'.format(num))
