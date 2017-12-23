# coding:utf-8

import unittest
import json
import os
from common import common
from common.login import Login
from common import custom


class CWD(unittest.TestCase):
	'''车位贷用例'''
	
	def setUp(self):
		self.page = Login()
		self.applyCode = ''
		self.next_user_id = ""
		local_dir = os.getcwd()
		print("local_dir: %s " % local_dir)
		
		# 环境初始化
		# self._enviroment_change(0)
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
			data, company = custom.enviroment_change(filename, self.number, self.env)
			# 录入的源数据
			self.data = data
			# 分公司选择
			self.company = company
		except Exception as e:
			print('load config error:', str(e))
			raise
	
	def _enviroment_change(self, i):
		'''
			环境切换
		:param i:   分公司序号  "0" 广州， "1" 长沙
		:return:
		'''
		# 导入数据
		import config
		rd = config.__path__[0]
		config_env = os.path.join(rd, 'env.json')
		data_config = os.path.join(rd, "data_cwd.json")
		with open(data_config, 'r') as f:
			self.data = json.load(f)
			print(self.data['applyVo']['productName'])
		
		# 环境变量, 切换分公司
		with open(config_env, 'r') as f1:
			self.env = json.load(f1)
			self.company = self.env["SIT"]["company"][i]
	
	def tearDown(self):
		self.page.quit()
	
	def skipTest(self, reason):
		pass
	
	def test_cwd_01_base_info(self):
		'''客户基本信息录入'''
		
		common.input_customer_base_info(self.page, self.data['applyVo'])
	
	def test_cwd_02_borrowr_info(self):
		'''借款人/共贷人/担保人信息'''
		
		self.test_cwd_01_base_info()
		common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])
	
	def test_cwd_03_Property_info(self):
		'''物业信息录入'''
		
		self.test_cwd_02_borrowr_info()
		common.input_cwd_bbi_Property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
	
	def test_cwd_04_applydata(self):
		'''申请件录入,提交'''
		
		# 1 客户信息-业务基本信息
		# log_to().info(u"客户基本信息录入")
		common.input_customer_base_info(self.page, self.data['applyVo'])
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		# log_to().info(u"借款人/共贷人信息录入")
		common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])
		
		# 3 物业信息
		# log_to().info(u"物业基本信息录入")
		common.input_cwd_bbi_Property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		
		# 提交
		common.submit(self.page)
	
	def test_cwd_05_get_applyCode(self):
		'''申请件查询'''
		
		self.test_cwd_04_applydata()
		applycode = common.get_applycode(self.page, self.data['custInfoVo'][0]['custName'])
		if applycode:
			self.applyCode = applycode
			return applycode, True
		else:
			return None, False
	
	def test_cwd_06_show_task(self):
		'''查看待处理任务列表'''
		
		result = self.test_cwd_05_get_applyCode()[0]
		res = common.query_task(self.page, result)
		if res:
			return True
		else:
			return False
	
	def test_cwd_07_process_monitor(self):
		'''流程监控'''
		
		result = self.test_cwd_05_get_applyCode()  # 申请件查询
		res = common.process_monitor(self.page, result[0])  # l流程监控
		
		if not res:
			return False
		else:
			self.page.user_info['auth']["username"] = res  # 更新下一个登录人
			print self.page.user_info['auth']["username"]
			self.next_user_id = res
			return res, result[0]  # (下一个处理人ID, 申请件ID)
	
	def test_cwd_08_branch_supervisor_approval(self):
		'''分公司主管审批'''
		
		# 获取分公司登录ID
		res = self.test_cwd_07_process_monitor()
		print "userId:" + res[0]
		
		# 下一个处理人重新登录
		page = Login(res[0])
		
		# 审批审核
		common.approval_to_review(page, res[1], u'分公司主管同意审批')
		
		# 查看下一步处理人
		next_id = common.process_monitor(page, self.applyCode)
		if not res:
			return False
		else:
			self.next_user_id = next_id
			# 当前用户退出系统
			self.page.driver.quit()
			return next_id  # 下一步处理人ID
	
	def test_cwd_09_branch_manager_approval(self):
		'''分公司经理审批'''
		
		# 获取分公司经理登录ID
		next_id = self.test_cwd_08_branch_supervisor_approval()
		
		# 下一个处理人重新登录
		page = Login(next_id)
		
		# 审批审核
		common.approval_to_review(page, self.applyCode, u'分公司经理同意审批')
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode)
		if not res:
			return False
		else:
			self.next_user_id = res
			# 当前用户退出系统
			self.page.driver.quit()
			return res
	
	def test_cwd_10_regional_prereview(self):
		'''区域预复核审批'''
		
		# 获取区域预复核员ID
		next_id = self.test_cwd_09_branch_manager_approval()
		
		# 下一个处理人重新登录
		page = Login(next_id)
		
		# 审批审核
		common.approval_to_review(page, self.applyCode, u'区域预复核通过')
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode)
		if not res:
			return False
		else:
			self.next_user_id = res
			# 当前用户退出系统
			self.page.driver.quit()
			return res
	
	def test_cwd_11_manager_approval(self):
		'''审批经理审批'''
		
		# 获取审批经理ID
		next_id = self.test_cwd_10_regional_prereview()
		
		# 下一个处理人重新登录
		page = Login(next_id)
		
		# 审批审核
		common.approval_to_review(page, self.applyCode, u'审批经理审批')
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode)
		if not res:
			return False
		else:
			self.next_user_id = res
			# 当前用户退出系统
			self.page.driver.quit()
			return res
	
	def test_cwd_12_contract_signing(self):
		'''签约'''
		
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
		
		# 获取合同打印专员ID
		next_id = self.test_cwd_11_manager_approval()
		
		# 下一个处理人重新登录
		page = Login(next_id)
		
		# 签约
		common.make_signing(page, i_frame, self.applyCode, rec_bank_info)
		# common.make_signing(self.page, i_frame, 'GZ20171207E15', rec_bank_info)
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode)
		if not res:
			return False
		else:
			self.next_user_id = res
			# 当前用户退出系统
			self.page.driver.quit()
			return res
	
	def test_cwd_13_compliance_audit(self):
		'''合规审查'''
		
		# 获取下一步合同登录ID
		next_id = self.test_cwd_12_contract_signing()
		
		# 下一个处理人重新登录
		page = Login(next_id)
		
		# 合规审查
		common.compliance_audit(page, self.applyCode)
	
	def test_cwd_14_authority_card_member_transact(self):
		'''权证办理'''
		
		# print  u"申请编号:" + self.applyCode
		# 合规审查
		self.test_cwd_13_compliance_audit()
		# 权证员登录
		page = Login(self.company["authority_member"]["user"])
		# 权证员上传权证信息
		common.authority_card_transact(page, self.applyCode)
		# common.authority_card_transact(page, "GZ20171213C06")
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode)
		if not res:
			return False
		else:
			self.next_user_id = res
			# 当前用户退出系统
			self.page.driver.quit()
			return res
	
	def test_cwd_15_warrant_apply(self):
		'''权证请款-原件请款'''
		
		# 获取合同打印专员ID
		next_id = self.test_cwd_14_authority_card_member_transact()
		page = Login(next_id)
		# 权证请款
		common.warrant_apply(page, self.applyCode)
	
	# page = Login('xn052298')
	# common.warrant_apply(page, "CS20171214X07")
	
	
	def test_cwd_16_finace_transact(self):
		'''财务办理'''
		
		# 权证请款
		self.test_cwd_15_warrant_apply()
		# 业务助理登录
		page = Login(self.company["business_assistant"]["user"])
		common.finace_transact(page, self.applyCode)
		
		# page = Login('xn052298')
		# common.finace_transact(page, 'CS20171215C02')
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode, 1)
		if not res:
			return False
		else:
			self.next_user_id = res
			# 当前用户退出系统
			self.page.driver.quit()
			return res
	
	def test_cwd_17_finace_approve_branch_manager(self):
		'''财务分公司经理审批'''
		
		remark = u"财务分公司经理审批"
		
		# 下一个处理人
		self.test_cwd_16_finace_transact()
		page = Login(self.next_user_id)
		result = common.finace_approve(page, self.applyCode, remark)
		if not result:
			return False
		
		# page = Login('xn028154')
		# common.finace_approve(page, "CS20171215X14", remark)
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode, 1)
		if not res:
			return False
		else:
			self.next_user_id = res
			print("nextId:" + res)
			# 当前用户退出系统
			self.page.driver.quit()
			return res
	
	def test_cwd_18_finace_approve_risk_control_manager(self):
		'''财务风控经理审批'''
		
		remark = u'风控经理审批'
		
		self.test_cwd_17_finace_approve_branch_manager()
		page = Login(self.next_user_id)
		common.finace_approve(page, self.applyCode, remark)
		
		# page = Login('xn003625')
		# common.finace_approve(page, "CS20171215X14", remark)
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode, 1)
		if not res:
			return False
		else:
			self.next_user_id = res
			print("nextId:" + self.next_user_id)
			# 当前用户退出系统
			self.page.driver.quit()
			return res
	
	def test_cwd_19_finace_approve_financial_accounting(self):
		'''财务会计审批'''
		
		remark = u'财务会计审批'
		
		self.test_cwd_18_finace_approve_risk_control_manager()
		page = Login(self.next_user_id)
		common.finace_approve(page, self.applyCode, remark)
		#
		# page = Login('xn037166')
		# common.finace_approve(page, "CS20171215X09", remark)
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode, 1)
		if not res:
			return False
		else:
			self.next_user_id = res
			print("nextId:" + self.next_user_id)
			# 当前用户退出系统
			self.page.driver.quit()
			return res
	
	def test_cwd_20_finace_approve_financial_manager(self):
		'''财务经理审批'''
		
		remark = u'财务经理审批'
		
		self.test_cwd_19_finace_approve_financial_accounting()
		page = Login(self.next_user_id)
		common.finace_approve(page, self.applyCode, remark)
	
	# page = Login('xn0007533')
	# common.finace_approve(page, "CS20171215X09", remark)
	
	
	def test_cwd_21_funds_raise(self):
		'''资金主管募资审批'''
		
		remark = u'资金主管审批'
		
		self.test_cwd_20_finace_approve_financial_manager()
		page = Login('xn0007533')
		common.funds_raise(page, self.applyCode, remark)
