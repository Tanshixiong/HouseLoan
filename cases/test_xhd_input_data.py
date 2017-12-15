# coding:utf-8

'''
    过桥通录单流程
'''

import random
import time
import unittest

from common import common
from common.login import Login
from common.custom import getName


class XHD(unittest.TestCase):
	def _init_params(self):
		self.cust_info = dict(
				_borrow_info=dict(
						custName=getName(),
						idNum="360101199101011054",
						phone="13564789215",
						address=u"湖南长沙",
						companyName=u'小牛普惠管理有限公司',
						postName=u'工程师',
						workDate=u'2011-02-03',  # 入职日期
						workYear=5,  # 工作年限
						monthIncoming=15000  # 月均收入
						),
				_cust_base_info=dict(
						productName=u'循环贷-1.0',  # 贷款产品
						applyAmount=50000,  # 申请金额
						applyPeriod=10,  # 贷款天数
						branchManager=u"小明",
						branchManagerCode="xn111",
						teamGroup=u"A队",
						teamGroupCode="xn0001",
						teamManager=u"小王",
						teamManagerCode="xn0001",
						sale=u"王刚",
						saleCode="xn0002",
						monthIncome=3000,
						checkApprove=u"同意",
						)
				)
		
		self.property_info = dict(
				propertyOwner=self.cust_info['_borrow_info']['custName'],
				propertyNo="ABCDEFG",
				)
	
	def setUp(self):
		self._init_params()
		self.page = Login()
	
	def tearDown(self):
		self.page.quit()
	
	'''
		  循环贷案件数据录入
	'''
	
	def test_xhd_01_base_info(self):
		'''客户基本信息录入'''
		common.input_customer_base_info(self.page, self.cust_info['_cust_base_info'])
	
	def test_xhd_02_borrowr_info(self):
		'''借款人/共贷人/担保人信息'''
		common.input_customer_base_info(self.page, self.cust_info['_cust_base_info'])
		common.input_customer_borrow_info(self.page, self.cust_info['_borrow_info'])
	
	def test_xhd_03_Property_info(self):
		'''物业信息录入'''
		common.input_customer_base_info(self.page, self.cust_info['_cust_base_info'])
		common.input_customer_borrow_info(self.page, self.cust_info['_borrow_info'])
		common.input_bbi_Property_info(self.page)
	
	def test_xhd_04_applydata(self):
		'''申请件录入,提交'''
		
		# 1 客户信息-业务基本信息
		# log_to().info(u"客户基本信息录入")
		common.input_customer_base_info(self.page, self.cust_info['_cust_base_info'])
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		# log_to().info(u"借款人/共贷人信息录入")
		common.input_customer_borrow_info(self.page, self.cust_info['_borrow_info'])
		
		# 3 物业信息
		# log_to().info(u"物业基本信息录入")
		common.input_bbi_Property_info(self.page)
		
		# 提交
		common.submit(self.page)
	
	def test_xhd_05_get_applyCode(self):
		'''申请件查询'''
		
		self.test_xhd_04_applydata()
		name = self.cust_info['_borrow_info']['custName']
		applycode = common.get_applycode(self.page, name)
		if applycode:
			return applycode, True
		else:
			return None, False
	
	def test_xhd_06_show_task(self):
		'''查看待处理任务列表'''
		result = self.test_xhd_05_get_applyCode()[0]
		res = common.query_task(self.page, result)
		if res:
			return True
		else:
			return False


if __name__ == '__main__':
	unittest.main()
