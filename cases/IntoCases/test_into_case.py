# coding:utf-8
import unittest
import time
import json
import os
from common import common
from common.custom import enviroment_change
from common.login import Login


class IntoCase(unittest.TestCase, Login):
	def setUp(self):
		with open("E:/HouseLoanAuto/config/env.json", 'r') as f:
			self.da = json.load(f)
			self.number = self.da["number"]
			self.env = self.da["enviroment"]
		
		filename = "data_cwd.json"
		data, company = enviroment_change(filename, self.number, self.env)
		# self.page = Login.__init__(self)
		self.page = Login()
		# 录入的源数据
		self.data = data
		# 分公司选择
		self.company = company
	
	def tearDown(self):
		pass
	
	def test_01_one_borrower(self):
		print(self.data)
		print(self.company)
		common.input_customer_base_info(self.page, self.data['applyVo'])
		common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])
	
	def test_02(self):
		self.skipTest("xxxxx")
		print("ok")


if __name__ == '__main__':
	
	ic = IntoCase()
# suite = unittest.TestSuite()
# suite.addTest(IntoCase('test_01_one_borrower'))
# runner = unittest.TextTestRunner()
# runner.run(suite)
