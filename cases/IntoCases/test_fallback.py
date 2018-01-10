# coding:utf-8

import unittest
import time
import json
import os
from common import common
from common.login import Login
from common.custom import Log, enviroment_change


class fallback(unittest.TestCase):
	def setUp(self):
		try:
			import config
			rootdir = config.__path__[0]
			config_env = os.path.join(rootdir, 'env.json')
			print("config_env:" + config_env)
			with open(config_env, 'r') as f:
				self.da = json.load(f)
				self.number = self.da["number"]
				self.env = self.da["enviroment"]
			
			filename = "data_cwd.json"
			data, company = enviroment_change(filename, self.number, self.env)
			# self.page = Login.__init__(self)
			self.page = Login()
			self.log = Log()
			
			# 录入的源数据
			self.data = data
			# 分公司选择
			self.company = company
		except Exception as e:
			print('load config error:', str(e))
			raise
	
	def tearDown(self):
		pass
	
	def test_01_director_fallback(self):
		'''主管回退'''
		# 1 客户信息-业务基本信息
		if common.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])
		
		# 3 物业信息
		common.input_cwd_bbi_Property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applycode = common.get_applycode(self.page, self.data['custInfoVo'][0]['custName'])
		
		if applycode:
			self.applyCode = applycode
			self.log.info("申请件查询完成")
			print("applyCode:" + self.applyCode)
		res = common.query_task(self.page, applycode)
		if res:
			self.log.info("查询待处理任务成功")
		else:
			self.log.error(u"查询待处理任务失败")
		
		result = common.process_monitor(self.page, res)
		self.page.user_info['auth']["username"] = res  # 更新下一个登录人
		print self.page.user_info['auth']["username"]
		self.next_user_id = res
		self.log.info("完成流程监控查询")
		
		# 下一个处理人重新登录
		page = Login(result)
		
		res = common.approval_to_review(page, res[1], u'分公司主管同意审批')
		if not res:
			self.log.error("can't find applycode")
			raise ValueError("can't find applycode")
		
		next_id = common.process_monitor(page, self.applyCode)
		if not res:
			return False
		else:
			self.next_user_id = next_id
			self.log.info("风控审批-分公司主管审批结束")
			# 当前用户退出系统
			self.page.driver.quit()
			return next_id  # 下一步处理人ID
	
	def test_02_manager_fallback(self):
		'''经理回退'''
