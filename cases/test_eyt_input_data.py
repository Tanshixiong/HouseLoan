# coding:utf-8

'''
    E押通录单流程
'''

import random
import unittest

from common import common
from common.login import Login
from common.custom import getName, logout


class EYT(unittest.TestCase):
	'''E押通-2.0产品测试'''
	
	def _init_params(self):
		self.cust_info = {
			'_cust_base_info': {
				'productName': u'E押通-2.0(二押)',  # 贷款产品
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
		
		self.property_info = {
			'propertyOwner': self.cust_info['_borrow_info']['custName'],  # 产权人
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
		name = self.cust_info['_borrow_info']['custName']
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
		
		# 下一个处理人重新登录
		page = Login(res[0])
		
		# 审批审核
		common.approval_to_review(page, res[1], u'分公司主管同意审批')
		
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
		common.approval_to_review(page, self.cust_info['applyCode'], u'分公司经理同意审批')
		
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
		common.approval_to_review(page, self.cust_info['applyCode'], u'区域预复核通过')
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.cust_info['applyCode'])
		if not res:
			return False
		else:
			self.cust_info['next_user_id'] = res
			# 当前用户退出系统
			self.page.driver.quit()
			return res
	
	def test_eyt_11_manager_approval(self):
		'''审批经理审批'''
		
		# 获取审批经理ID
		next_id = self.test_eyt_10_regional_prereview()
		
		# 下一个处理人重新登录
		page = Login(next_id)
		
		# 审批审核
		common.approval_to_review(page, self.cust_info['applyCode'], u'审批经理审批')
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.cust_info['applyCode'])
		if not res:
			return False
		else:
			self.cust_info['next_user_id'] = res
			# 当前用户退出系统
			self.page.driver.quit()
			return res
	
	def test_12_contract_signing(self):
		'''签约'''
		
		i_frame = 'bTabs_tab_house_commonIndex_todoList'
		# 收款银行信息
		rec_bank_info = dict(
				recBankNum='6210302082441017886',
				recPhone='13686467482',
				recBankProvince=u'湖南省',
				recBankDistrict=u'长沙',
				recBank=u'中国农业银行',
				recBankBranch=u'北京支行',
				)
		
		# 扣款银行信息
		rep_bank_info = dict(
				rep_name=u'习近平',
				rep_id_num='420101198201013526',
				rep_bank_code='6210302082441017886',
				rep_phone='13686467482',
				provice=u'湖南省',
				district=u'长沙',
				rep_bank_name=u'中国银行',
				rep_bank_branch_name=u'北京支行',
				)
		
		# 获取合同打印专员ID
		next_id = self.test_eyt_11_manager_approval()
		
		# 下一个处理人重新登录
		page = Login(next_id)
		
		# 签约
		common.make_signing(page, i_frame, self.cust_info['applyCode'], rec_bank_info)
		# common.make_signing(self.page, i_frame, 'GZ20171207E15', rec_bank_info)
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.cust_info['applyCode'])
		if not res:
			return False
		else:
			self.cust_info['next_user_id'] = res
			# 当前用户退出系统
			self.page.driver.quit()
			return res
	
	def test_13_compliance_audit(self):
		'''合规审查'''
		
		i_frame = 'bTabs_tab_house_commonIndex_todoList'
		# 获取下一步合同登录ID
		next_id = self.test_12_contract_signing()
		
		# 下一个处理人重新登录
		page = Login(next_id)
		
		# 合规审查
		common.compliance_audit(page, self.cust_info['applyCode'])


if __name__ == '__main__':
	unittest.main()
