# coding:utf-8
import os
import time
import unittest
import sys
# from HTMLTestRunner import HTMLTestRunner
from HTMLTestRunnerCN import HTMLTestRunner

from cases import test_gqt_input_data
from cases import test_eyt_input_data
from cases import test_xhd_input_data
from cases import test_suite_cwd

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == "__main__":
	def set_reporter_path():
		# 定义报告存放路径以及格式
		# local_dir = os.path.dirname(os.getcwd())
		# local_dir = os.getcwd()
		local_dir = "E:\HouseLoanAuto"
		print("local_dir: %s " % local_dir)
		path = local_dir + "\log\\" + now + "-result.html"
		print("path:", path)
		return local_dir, path


	# 按照一定格式获取当前时间
	now = time.strftime("%Y-%m-%d %H_%M_%S")
	PT = set_reporter_path()
	print("path:", PT)
	fp = open(PT[1], 'wb')

	suite = unittest.TestSuite()
	# 构造测试套件
	#过桥通产品
	suite.addTest(test_gqt_input_data.GQT('test_gqt_01'))

	#E押通产品
	suite.addTest(test_eyt_input_data.EYT('test_eyt_01_base_info'))
	suite.addTest(test_eyt_input_data.EYT('test_ety_02_borrowr_info'))
	suite.addTest(test_eyt_input_data.EYT('test_eyt_03_Property_info'))
	suite.addTest(test_eyt_input_data.EYT('test_eyt_04_applydata'))
	suite.addTest(test_eyt_input_data.EYT('test_eyt_05_get_applyCode'))
	suite.addTest(test_eyt_input_data.EYT('test_eyt_06_show_task'))
	suite.addTest(test_eyt_input_data.EYT('test_eyt_07_process_monitor'))
	suite.addTest(test_eyt_input_data.EYT('test_eyt_08_branch_supervisor_approval'))
	suite.addTest(test_eyt_input_data.EYT('test_eyt_09_branch_manager_approval'))
	suite.addTest(test_eyt_input_data.EYT('test_eyt_10_regional_prereview'))
	suite.addTest(test_eyt_input_data.EYT('test_eyt_11_manager_approval'))
	suite.addTest(test_eyt_input_data.EYT('test_12_contract_signing'))
	suite.addTest(test_eyt_input_data.EYT('test_13_compliance_audit'))
	suite.addTest(test_eyt_input_data.EYT('test_quit_system'))
	
	#循环贷产品
	suite.addTest(test_xhd_input_data.XHD('test_xhd_01_base_info'))
	suite.addTest(test_xhd_input_data.XHD('test_xhd_02_borrowr_info'))
	suite.addTest(test_xhd_input_data.XHD('test_xhd_03_Property_info'))
	suite.addTest(test_xhd_input_data.XHD('test_xhd_04_applydata'))
	suite.addTest(test_xhd_input_data.XHD('test_xhd_05_get_applyCode'))
	suite.addTest(test_xhd_input_data.XHD('test_xhd_06_show_task'))
	runner = unittest.TextTestRunner()
	
	# 车位贷
	suite.addTest(test_suite_cwd.CWD('test_cwd_01_base_info'))
	suite.addTest(test_suite_cwd.CWD('test_cwd_02_borrowr_info'))
	suite.addTest(test_suite_cwd.CWD('test_cwd_03_Property_info'))
	suite.addTest(test_suite_cwd.CWD('test_cwd_04_applydata'))
	suite.addTest(test_suite_cwd.CWD('test_cwd_05_get_applyCode'))
	suite.addTest(test_suite_cwd.CWD('test_cwd_06_show_task'))
	suite.addTest(test_suite_cwd.CWD('test_cwd_07_process_monitor'))
	suite.addTest(test_suite_cwd.CWD('test_cwd_08_branch_supervisor_approval'))
	suite.addTest(test_suite_cwd.CWD('test_cwd_09_branch_manager_approval'))
	suite.addTest(test_suite_cwd.CWD('test_cwd_10_regional_prereview'))
	suite.addTest(test_suite_cwd.CWD('test_cwd_11_manager_approval'))
	suite.addTest(test_suite_cwd.CWD('test_cwd_12_contract_signing'))
	suite.addTest(test_suite_cwd.CWD('test_cwd_13_compliance_audit'))
	suite.addTest(test_suite_cwd.CWD('test_cwd_14_authority_card_member_transact'))
	suite.addTest(test_suite_cwd.CWD('test_cwd_15_warrant_apply'))
	suite.addTest(test_suite_cwd.CWD('test_cwd_16_finace_transact'))


	# 定义测试报告
	runner = HTMLTestRunner(stream=fp, title='测试报告', description='用例执行情况:')
	# import pdb
	# pdb.set_trace()
	runner.run(suite)

	fp.close()  # 关闭测试报告
