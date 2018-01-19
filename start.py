# coding:utf-8
import os
import time
import unittest
import sys
import yaml
# from HTMLTestRunner import HTMLTestRunner
from HTMLTestRunnerCN import HTMLTestRunner
from cases.baseProcess import (
	test_suite_cwd,
	test_eyt_input_data,
	test_xhd_input_data,
	test_gqt_input_data
	)
from cases.IntoCases import (
	test_into_case,
	test_fallback
	)
from cases.contract_sigining import test_more_person_sign

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == "__main__":
	
	def set_reporter_path():
		# 定义报告存放路径以及格式
		# local_dir = os.path.dirname(os.getcwd())
		# local_dir = os.getcwd()
		local_dir = "E:\HouseLoanAuto"
		print("local_dir: %s " % local_dir)
		# path = local_dir + "\\report\\" + now + "-result.html"
		path = local_dir + "\\report\\" + "index.html"
		return local_dir, path
	
	
	# 按照一定格式获取当前时间
	now = time.strftime("%Y-%m-%d %H_%M_%S")
	PT = set_reporter_path()
	print("path:", PT)
	fp = open(PT[1], 'wb')
	
	# 创建测试套
	suite = unittest.TestSuite()
	
	#  以下方法会报错， 原因不明
	# try:
	# 	import config
	#
	# 	rootdir = config.__path__[0]
	# 	fp = os.path.join(rootdir, 'caseNumber.yaml')
	# 	with open(fp, 'r') as f:
	# 		temp = yaml.load(f)
	# except Exception as e:
	# 	print "Error: can't load file"
	# 	raise
	
	with open("E:\HouseLoanAuto\config\caseNumber.yaml", 'r') as f:
		temp = yaml.load(f)
		# 车位贷用例
		for i in temp['cwd']:
			suite.addTest(test_suite_cwd.CWD(i))
		# E押通用例
		for i in temp['eyt']:
			suite.addTest(test_eyt_input_data.EYT(i))
		# 循环贷用例
		for i in temp['xhd']:
			suite.addTest(test_xhd_input_data.XHD(i))
		# 过桥通用例
		for i in temp['gqt']:
			suite.addTest(test_gqt_input_data.GQT(i))
		# 进件场景
		for i in temp['IntoCase']:
			suite.addTest(test_into_case.IntoCase(i))
		# 回退场景
		for i in temp['fallback']:
			suite.addTest(test_fallback.fallback(i))
		# 签约
		for i in temp['contract']:
			suite.addTest(test_more_person_sign.contractSign(i))

	# 定义测试报告
	runner = HTMLTestRunner(stream=fp, title='测试报告', description='用例执行情况:')
	# import pdb
	# pdb.set_trace()
	runner.run(suite)
	
	fp.close()  # 关闭测试报告
