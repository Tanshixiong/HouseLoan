# coding:utf-8

'''
    过桥通录单流程
'''

import random
import unittest

from common import common
from common.login import Login
from common.custom import getName


class GQT(unittest.TestCase):
	'''过桥通-1.0产品测试'''
	def _init_params(self):
		# self.cust_info = dict(
		# 	_borrow_info=dict(
		# 		name= getName(),
		# 		id_num="360101199101011054",
		# 		phone="13564789215",
		# 		address=u"湖南长沙",
		# 		company=u'小牛普惠管理有限公司',
		# 		job=u'工程师',
		# 		entry_date=u'2011-02-03',  # 入职日期
		# 		work_year=5,  # 工作年限
		# 		monthly_incoming=15000  # 月均收入
		# 	),
		# 	_cust_base_info=dict(
		# 		product=u'过桥通-1.0(一线城市)',  # 贷款产品
		# 		apply_amount=50000,  # 申请金额
		# 		apply_period=10,  # 贷款天数
		# 		branch_manager_name=u"小明",
		# 		branch_manager="xn111",
		# 		apply_module_team_group_name=u"A队",
		# 		team_manager_name=u"小王",
		# 		team_manager="xn0001",
		# 		sale_name=u"王刚",
		# 		module_sale="xn0002",
		# 		module_month_income=3000,
		# 		checkApprove=u"同意",
		# 	)
		# )
		
		self.cust_info = {
			'_cust_base_info': {
				'productName': u'过桥通-1.0(一线城市)',  # 贷款产品
				'applyAmount': 200000,  # 申请金额
				'applyPeriod': 36,  # 贷款期数
				'branchManager': u"小明",
				'branchManagerCode': "xn111",
				'teamGroup': u"A队",
				"teamGroupCode": "xn0001",
				'teamManager': u"小王",
				'teamManagerCode': "xn0001",
				'sale': u"王刚",
				'saleCode': "xn0002",
				'monthIncome': 3000,
				'checkApprove': u"同意",
				},
			'_borrow_info': {
				'custName': getName(),
				'idNum': '360101199101011054',
				'phone': "13564789215",
				'address': u"湖南长沙",
				'companyName': u'小牛普惠管理有限公司',
				'postName': u'工程师',
				'workDate': u'2011-02-03',  # 入职日期
				'workYear': 5,  # 工作年限
				'monthIncoming': 15000  # 月均收入
				},
			'applyCode': '',
			'next_user_id': '',
			}
		self.loan_amount = 200000  # 拆分金额

	def setUp(self):
		self.page = Login()
		self._init_params()


	def tearDown(self):
		self.page.quit()

	'''
		  过桥通案件数据录入
	'''
	# 测试
	def test_gqt_01(self):
		# 1 客户信息-业务基本信息
		common.input_customer_base_info(self.page, self.cust_info['_cust_base_info'])

		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		common.input_customer_borrow_info(self.page, self.cust_info['_borrow_info'])


if __name__ == '__main__':
	unittest.main()
