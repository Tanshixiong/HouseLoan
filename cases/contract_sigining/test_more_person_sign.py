# coding:utf-8

import unittest
import time
import json
import os
from common import common
from common.login import Login
from common.custom import Log, enviroment_change


class contractSign(unittest.TestCase):
	'''合同签约'''
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
			self.page = Login()
			self.log = Log()
			
			# 录入的源数据
			self.data = data
			# 分公司选择
			self.company = company
		except Exception as e:
			self.log.error('load config error:', str(e))
			raise
	
	def get_next_user(self, page, applyCode, remark):
		next_id = common.process_monitor(page, applyCode)
		if next_id is None:
			self.log.error("没有找到下一步处理人！")
			raise
		else:
			self.next_user_id = next_id
			self.log.info(remark)
			self.log.info("下一步处理人:" + next_id)
			# 当前用户退出系统
			self.page.driver.quit()
	
	def tearDown(self):
		pass
	
	def test_one_person_sign(self):
		'''单人签约'''
		
		# ---------------------------------------------------------------------------------
		#                   1. 申请录入
		# ---------------------------------------------------------------------------------
		
		# 1 客户信息-业务基本信息
		if common.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.custName = common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])[1]
		
		# 3 物业信息
		common.input_cwd_bbi_Property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applyCode = common.get_applycode(self.page, self.custName)
		if applyCode:
			self.applyCode = applyCode
			self.log.info("申请件查询完成")
			print("applyCode:" + self.applyCode)
		# 流程监控
		result = common.process_monitor(self.page, applyCode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
		else:
			self.log.error("流程监控查询出错！")
			raise
		
		# ---------------------------------------------------------------------------------------
		# 	                        2. 风控审批流程
		# ---------------------------------------------------------------------------------------
		
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = common.approval_to_review(page, applyCode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise
		
		self.get_next_user(page, applyCode, u'分公司主管审批通过！')
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批
		res = common.approval_to_review(page, applyCode, u'分公司经理回退到申请录入', 0)
		if not res:
			self.log.error("审批失败")
			raise
		
		self.get_next_user(page, applyCode, u'分公司经理审批通过！')
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核审批
		res = common.approval_to_review(page, applyCode, u'区域预复核审批通过', 0)
		if not res:
			self.log.error("区域预复核审批失败！")
			raise
		
		self.get_next_user(page, applyCode, u'区域预复核审批通过！')
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批经理审批通过
		res = common.approval_to_review(page, applyCode, u'审批经理审批通过', 0)
		if not res:
			self.log.error("审批经理审批失败！")
			raise
		
		self.get_next_user(page, applyCode, u'审批经理审批成功！')
		
		# -----------------------------------------------------------------------------
		# 	                        3. 合同打印
		# -----------------------------------------------------------------------------
		
		i_frame = 'bTabs_tab_house_commonIndex_todoList'
		
		rec_bank_info = dict(
				recBankNum=self.data['houseCommonLoanInfoList'][0]['recBankNum'],
				recPhone=self.data['houseCommonLoanInfoList'][0]['recPhone'],
				recBankProvince=self.data['houseCommonLoanInfoList'][0]['recBankProvince'],
				recBankDistrict=self.data['houseCommonLoanInfoList'][0]['recBankDistrict'],
				recBank=self.data['houseCommonLoanInfoList'][0]['recBank'],
				recBankBranch=self.data['houseCommonLoanInfoList'][0]['recBankBranch'],
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
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 签约
		common.make_signing(page, self.applyCode, rec_bank_info)
		
		# 查看下一步处理人
		self.get_next_user(page, applyCode, u'合同打印完成！')
	
	def test_two_person_sign(self):
		'''两人签约'''
		
		# ---------------------------------------------------------------------------------
		#                   1. 申请录入
		# ---------------------------------------------------------------------------------
		
		self.data['applyVo']['applyAmount'] = 400000
		# 1 客户信息-业务基本信息
		if common.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.custName = common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])[1]
		
		# 3 物业信息
		common.input_cwd_bbi_Property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applyCode = common.get_applycode(self.page, self.custName)
		if applyCode:
			self.applyCode = applyCode
			self.log.info("申请件查询完成")
			print("applyCode:" + self.applyCode)
		# 流程监控
		result = common.process_monitor(self.page, applyCode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
		else:
			self.log.error("流程监控查询出错！")
			raise
		
		# ---------------------------------------------------------------------------------------
		# 	                        2. 风控审批流程
		# ---------------------------------------------------------------------------------------
		
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = common.approval_to_review(page, applyCode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise
		
		self.get_next_user(page, applyCode, u'分公司主管审批通过！')
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批
		res = common.approval_to_review(page, applyCode, u'分公司经理审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise
		
		self.get_next_user(page, applyCode, u'分公司经理审批通过！')
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核审批
		res = common.approval_to_review(page, applyCode, u'区域预复核审批通过', 0)
		if not res:
			self.log.error("区域预复核审批失败！")
			raise
		
		self.get_next_user(page, applyCode, u'区域预复核审批通过！')
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批经理审批通过
		res = common.approval_to_review(page, applyCode, u'审批经理审批通过', 0)
		if not res:
			self.log.error("审批经理审批失败！")
			raise
		
		self.get_next_user(page, applyCode, u'审批经理审批成功！')
		
		# -----------------------------------------------------------------------------
		# 	                        3. 合同打印
		# -----------------------------------------------------------------------------
		
		rec_bank_info = dict(
				recBankNum=self.data['houseCommonLoanInfoList'][0]['recBankNum'],
				recPhone=self.data['houseCommonLoanInfoList'][0]['recPhone'],
				recBankProvince=self.data['houseCommonLoanInfoList'][0]['recBankProvince'],
				recBankDistrict=self.data['houseCommonLoanInfoList'][0]['recBankDistrict'],
				recBank=self.data['houseCommonLoanInfoList'][0]['recBank'],
				recBankBranch=self.data['houseCommonLoanInfoList'][0]['recBankBranch'],
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
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 两个人签约
		common.make_signing(page, self.applyCode, rec_bank_info, 2)
		
		# 查看下一步处理人
		self.get_next_user(page, applyCode, u'合同打印完成！')
	
	
	def test_03_three_person_sign(self):
		'''三人签约'''
		
		# ---------------------------------------------------------------------------------
		#                   1. 申请录入
		# ---------------------------------------------------------------------------------
		
		self.data['applyVo']['applyAmount'] = 600000
		# 1 客户信息-业务基本信息
		if common.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.custName = common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])[1]
		
		# 3 物业信息
		common.input_cwd_bbi_Property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applyCode = common.get_applycode(self.page, self.custName)
		if applyCode:
			self.applyCode = applyCode
			self.log.info("申请件查询完成")
			print("applyCode:" + self.applyCode)
		# 流程监控
		result = common.process_monitor(self.page, applyCode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
		else:
			self.log.error("流程监控查询出错！")
			raise
		
		# ---------------------------------------------------------------------------------------
		# 	                        2. 风控审批流程
		# ---------------------------------------------------------------------------------------
		
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = common.approval_to_review(page, applyCode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise
		
		self.get_next_user(page, applyCode, u'分公司主管审批通过！')
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批
		res = common.approval_to_review(page, applyCode, u'分公司经理审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise
		
		self.get_next_user(page, applyCode, u'分公司经理审批通过！')
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核审批
		res = common.approval_to_review(page, applyCode, u'区域预复核审批通过', 0)
		if not res:
			self.log.error("区域预复核审批失败！")
			raise
		
		self.get_next_user(page, applyCode, u'区域预复核审批通过！')
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批经理审批通过
		res = common.approval_to_review(page, applyCode, u'审批经理审批通过', 0)
		if not res:
			self.log.error("审批经理审批失败！")
			raise
		
		self.get_next_user(page, applyCode, u'审批经理审批成功！')
		
		# -----------------------------------------------------------------------------
		# 	                        3. 合同打印
		# -----------------------------------------------------------------------------
		
		rec_bank_info = dict(
				recBankNum=self.data['houseCommonLoanInfoList'][0]['recBankNum'],
				recPhone=self.data['houseCommonLoanInfoList'][0]['recPhone'],
				recBankProvince=self.data['houseCommonLoanInfoList'][0]['recBankProvince'],
				recBankDistrict=self.data['houseCommonLoanInfoList'][0]['recBankDistrict'],
				recBank=self.data['houseCommonLoanInfoList'][0]['recBank'],
				recBankBranch=self.data['houseCommonLoanInfoList'][0]['recBankBranch'],
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
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 两个人签约
		common.make_signing(page, self.applyCode, rec_bank_info, 3)
		
		# 查看下一步处理人
		self.get_next_user(page, applyCode, u'合同打印完成！')