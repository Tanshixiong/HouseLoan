# coding:utf-8

'''
    E押通录单流程
'''

import random
import unittest

from common import common
from common.login import Login
from common.model import getName, logout


class EYT(unittest.TestCase):
	'''E押通-2.0产品测试'''
	
	def _init_params(self):
		self.cust_info = {
			'_cust_base_info': {
				'product': u'E押通-2.0(一押)',  # 贷款产品
				'apply_amount': 500000,  # 申请金额
				'apply_period': 36,  # 贷款期数
				'branch_manager_name': u"小明",
				'branch_manager': "xn111",
				'apply_module_team_group_name': u"A队",
				'team_manager_name': u"小王",
				'team_manager': "xn0001",
				'sale_name': u"王刚",
				'module_sale': "xn0002",
				'module_month_income': 3000,
				'checkApprove': u"同意",
				},
			'_borrow_info': {
				'name': getName(),
				'id_num': '360101199101011054',
				'phone': "13564789215",
				'address': u"湖南长沙",
				'company': u'小牛普惠管理有限公司',
				'job': u'工程师',
				'entry_date': u'2011-02-03',  # 入职日期
				'work_year': 5,  # 工作年限
				'monthly_incoming': 15000  # 月均收入
				},
			'applyCode': '',
			'next_user_id': '',
			}
		
		self.property_info = {
			'propertyOwner': self.cust_info['_borrow_info']['name'],  # 产权人
			'propertyNo': 'EYT2017230',  # 房产证号
			'propertyStatus': True,  # 是否涉贷物业
			'propertyAge': 10,  # 房龄
			'propertyArea': 220,  # 建筑面积
			'registrationPrice': 333,  # 等级价
			'address': {
				'propertyAddressProvince': u'河北省',
				'propertyAddressCity': u'秦皇岛市',
				'propertyAddressDistinct': u'山海关区',
				'propertyAddressDetail': u'具体地址信息',
				},
			'evaluationSumAmount': 200,  # 评估公允价总值
			'evaluationNetAmount': 200,  # 评估公允价净值
			'slSumAmount': 202,  # 世联评估总值
			"slPrice": 203,  # 中介评估总值
			"agentSumAmout": 221,  # 中介评估净值
			"netSumAmount": 230,  # 网评总值
			"netAmount": 240,  # 网评净值
			"localSumAmount": 230,  # 当地评估总值
			"localNetValue": 290,  # 当地评估净值
			"remark": u"周边环境很好，带学位房，交通便利，风景秀丽.",  # 物业配套描述
			"localAssessmentOrigin": u'房产局',  # 当地评估来源
			"assessmentOrigin": u'世联行',  # 评估来源
			"evaluationCaseDescrip": u'好的没话说',  # 评估情况描述
			}
	
	def setUp(self):
		self._init_params()
		self.page = Login()
	
	def tearDown(self):
		self.page.quit()
	
	'''
		  E押通案件数据录入
	'''
	
	def test_eyt_01_base_info(self):
		'''客户基本信息录入'''
		common.input_customer_base_info(self.page, self.cust_info['_cust_base_info'])
	
	def test_ety_02_borrowr_info(self):
		'''借款人/共贷人/担保人信息'''
		common.input_customer_base_info(self.page, self.cust_info['_cust_base_info'])
		common.input_customer_borrow_info(self.page, self.cust_info['_borrow_info'])
	
	def test_eyt_03_Property_info(self):
		'''物业信息录入'''
		common.input_customer_base_info(self.page, self.cust_info['_cust_base_info'])
		common.input_customer_borrow_info(self.page, self.cust_info['_borrow_info'])
		common.input_bbi_Property_info(self.page)
	
	def test_eyt_04_applydata(self):
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
	
	def test_eyt_05_get_applyCode(self):
		'''申请件查询'''
		
		self.test_eyt_04_applydata()
		name = self.cust_info['_borrow_info']['name']
		applycode = common.get_applycode(self.page, name)
		if applycode:
			self.cust_info['applyCode'] = applycode
			return applycode, True
		else:
			return None, False
	
	def test_eyt_06_show_task(self):
		'''查看待处理任务列表'''
		result = self.test_eyt_05_get_applyCode()[0]
		res = common.query_task(self.page, result)
		if res:
			return True
		else:
			return False
	
	def test_eyt_07_process_monitor(self):
		'''流程监控'''
		result = self.test_eyt_05_get_applyCode()  # 申请件查询
		res = common.process_monitor(self.page, result[0])  # l流程监控
		
		if not res:
			return False
		else:
			self.page.user_info['auth']["username"] = res  # 更新下一个登录人
			print self.page.user_info['auth']["username"]
			self.cust_info['next_user_id'] = res
			return res, result[0]  # (下一个处理人ID, 申请件ID)
	
	def test_eyt_08_branch_supervisor_approval(self):
		'''分公司主管审批'''
		
		# 获取分公司登录ID
		res = self.test_eyt_07_process_monitor()
		print "userId:" + res[0]
		
		# 当前用户退出系统
		self.page.driver.close()
		
		# 下一个处理人重新登录
		page = Login(res[0])
		
		# 审批审核
		common.branch_supervisor_approval(page, res[1])
		
		# 查看下一步处理人
		next_id = common.process_monitor(page, self.cust_info['applyCode'])
		if not res:
			return False
		else:
			# self.page.user_info['auth']["username"] = res  # 更新下一个登录人
			# print self.page.user_info['auth']["username"]
			self.cust_info['next_user_id'] = next_id
			# 当前用户退出系统
			self.page.driver.quit()
			return next_id  # 下一步处理人ID
	
	def test_quit_system(self):
		'''退出系统'''
		logout(self.page.driver)
		self.page.driver.close()  # 关闭浏览器
	
	def test_eyt_09_branch_manager_approval(self):
		'''分公司经理审批'''
		
		# 获取分公司经理登录ID
		next_id = self.test_eyt_08_branch_supervisor_approval()
		
		# 下一个处理人重新登录
		page = Login(next_id)
		
		# 审批审核
		common.branch_manager_approval(page, self.cust_info['applyCode'])
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.cust_info['applyCode'])
		if not res:
			return False
		else:
			self.cust_info['next_user_id'] = res
			# 当前用户退出系统
			self.page.driver.quit()
			return res
	
	def test_eyt_10_regional_prereview(self):
		'''区域预复核审批'''
		
		# 获取区域预复核员ID
		next_id = self.test_eyt_09_branch_manager_approval()
		
		# 下一个处理人重新登录
		page = Login(next_id)
		
		# 审批审核
		common.regional_prereview(page, self.cust_info['applyCode'])
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.cust_info['applyCode'])
		if not res:
			return False
		else:
			self.cust_info['next_user_id'] = res
			# 当前用户退出系统
			self.page.driver.quit()
			return res


if __name__ == '__main__':
	unittest.main()
