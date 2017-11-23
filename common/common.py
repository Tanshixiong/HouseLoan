# coding:utf-8

'''
    通用方法
'''

import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

from config.locator import loc_cust_info, loc_borrower
from selenium.common import exceptions as EC


def browser(arg="chrome"):
	'''选择浏览器'''
	if arg == "ie":
		driver = webdriver.Firefox()
	elif arg == "chrome":
		driver = webdriver.Chrome()
	elif arg == "firefox":
		driver = webdriver.Firefox()
	else:
		raise "Can't support the kind of borrower!"
	
	return driver


# 客户基本信息录入
def input_customer_base_info(page, data):
	# 案件录入
	time.sleep(2)
	page._click_control(page.driver, "xpath", "html/body/header/ul/li[3]")
	time.sleep(2)
	page._click_control(page.driver, "xpath", "html/body/header/ul/li[3]/ul/li[1]/a")
	
	# 主界面
	# 切换表单(id="myIframe")或者(name="framing")
	# page.driver.switch_to.frame("myIframe") #切换到第一个frame
	page.driver.switch_to.frame("bTabs_tab_house_commonIndex_applyIndex_index")  # 切换到房贷申请录入iframe
	
	Select(page.driver.find_element_by_xpath(".//*[@id='apply_module_product_id']")).select_by_visible_text(
			data["product"])  # 产品
	page._send_data(page.driver, "id", loc_cust_info['je_id'], data["apply_amount"])  # 金额
	page._send_data(page.driver, "id", loc_cust_info['dkts_id'], data["apply_period"])  # 贷款天数
	page._send_data(page.driver, "id", loc_cust_info['fgsjlxm_id'], data["branch_manager_name"])  # 分公司经理姓名:
	page._send_data(page.driver, "id", loc_cust_info['fgsjlgh_id'], data["branch_manager"])  # 分公司经理工号
	page._send_data(page.driver, "id", loc_cust_info['tdzb_id'], data["apply_module_team_group_name"])  # 团队组别
	page._send_data(page.driver, "id", loc_cust_info['tdjlxm_id'], data["team_manager_name"])  # 团队经理姓名
	page._send_data(page.driver, "id", loc_cust_info['tdjlgh_id'], data["team_manager"])  # 团队经理工号
	page._send_data(page.driver, "id", loc_cust_info['khjlxm_id'], data["sale_name"])  # 客户经理姓名
	page._send_data(page.driver, "id", loc_cust_info['khjlgh_id'], data["module_sale"])  # 客户经理工号
	page._send_data(page.driver, "id", loc_cust_info['lsyjsr_id'], data["module_month_income"])  # 流水月均收入
	page._send_data(page.driver, "name", loc_cust_info['zyyjbz_name'], data["checkApprove"])  # 专员意见备注
	# 保存
	save(page)


# 借款人/担保人/共贷信息录入
def input_customer_borrow_info(page, data):
	'''
		客户基本信息 - 借款人/共贷人/担保人信息
	:param page 页面
	:param data 传入的数据
	:return:
	'''
	page._click_control(page.driver, "xpath", ".//*[@id='tb']/a[1]/span[2]")
	page.driver.find_element_by_css_selector(loc_borrower['jkrxm']).send_keys(unicode(data['name']))  # 借款人姓名
	time.sleep(1)
	page._send_data(page.driver, "xpath", loc_borrower['sfzhm'], data["id_num"])  # 身份证号码
	# 受教育程度
	page._click_control(page.driver, "id", loc_borrower['sjycd']['locate'])
	page._click_control(page.driver, "id", loc_borrower['sjycd']['value'])
	
	page._click_control(page.driver, "id", loc_borrower['hyzk']['locate'])  # 婚姻状况
	time.sleep(1)
	page._click_control(page.driver, "id", loc_borrower['hyzk']['value'])
	
	page._send_data(page.driver, "id", loc_borrower['jtdzxx'], data['address'])  # 家庭地址信息
	page._send_data(page.driver, "xpath", loc_borrower['xxfs'], data["phone"])  # 联系方式
	page._send_data(page.driver, "xpath", loc_borrower['dwmc'], data["company"])  # 单位名称
	
	# 公司规模
	# page.driver.find_element_by_css_selector(loc_borrower['gsgm']['a']).click()
	# page.driver.find_element_by_xpath(loc_borrower['gsgm']['a']).click()
	# page._click_control(page.driver, "xpath", loc_borrower['gsgm']['b'])
	# page._click_control(page.driver, "xpath", loc_borrower['gsgm']['c'])
	
	# 此处用这个方法
	page._click_control(page.driver, "id", loc_borrower['gsgm']['locate'])
	page._click_control(page.driver, "id", loc_borrower['gsgm']['value'])
	
	# 所属行业
	page._click_control(page.driver, "id", loc_borrower['sshy']['locate'])
	page._click_control(page.driver, "id", loc_borrower['sshy']['value'])
	
	page._send_data(page.driver, "id", loc_borrower['zw'], data["job"])  # 职位
	page._send_data(page.driver, "xpath", loc_borrower['rzrq'], data["entry_date"])  # 入职日期
	page._send_data(page.driver, "id", loc_borrower['gzyx'], data['work_year'])  # 工作年限
	page._send_data(page.driver, "id", loc_borrower['yjsr'], data['monthly_incoming'])  # 月均收入
	page.driver.find_element_by_css_selector("input[type=\"checkbox\"]").click()  # 是否有社保 Todo
	# 临时保存
	save(page)


# 输入多个借款人（待完善）
def input_more_borrower(page, data, num):
	'''
		客户基本信息 - 借款人/共贷人/担保人信息
	:param page 页面
	:param data 传入的数据
	:return:
	'''
	
	# self._click_control(page.driver, "xpath", "//div[@id='tb']/a/span[2]")
	page._click_control(page.driver, "xpath", ".//*[@id='tb']/a[1]/span[2]")
	
	page.driver.find_element_by_css_selector(loc_borrower['jkrxm']).send_keys(data['name'])  # 借款人姓名
	time.sleep(1)
	
	def action():
		# page.driver.find_element_by_css_selector(loc_borrower['jkrxm']).send_keys(data['name'])  # 借款人姓名
		# time.sleep(1)
		page._send_data(page.driver, "xpath", loc_borrower['sfzhm'], data["id_num"])  # 身份证号码
		# 受教育程度
		page._click_control(page.driver, "id", loc_borrower['sjycd']['locate'])
		page._click_control(page.driver, "id", loc_borrower['sjycd']['value'])
		
		page._click_control(page.driver, "id", loc_borrower['hyzk']['locate'])  # 婚姻状况
		page._click_control(page.driver, "id", loc_borrower['hyzk']['value'])
		
		page._send_data(page.driver, "id", loc_borrower['jtdzxx'], data['address'])  # 家庭地址信息
		page._send_data(page.driver, "xpath", loc_borrower['xxfs'], data["phone"])  # 联系方式
		page._send_data(page.driver, "xpath", loc_borrower['dwmc'], data["company"])  # 单位名称
		
		# 公司规模
		page.driver.find_element_by_css_selector(loc_borrower['gsgm']['a']).click()
		page._click_control(page.driver, "xpath", loc_borrower['gsgm']['b'])
		page._click_control(page.driver, "id", loc_borrower['gsgm']['c'])
		
		# 所属行业
		page._click_control(page.driver, "id", loc_borrower['sshy']['locate'])
		page._click_control(page.driver, "id", loc_borrower['sshy']['value'])
		
		page._send_data(page.driver, "id", loc_borrower['zw'], data["job"])  # 职位
		page._send_data(page.driver, "xpath", loc_borrower['rzrq'], data["entry_date"])  # 入职日期
		page._send_data(page.driver, "id", loc_borrower['gzyx'], data['work_year'])  # 工作年限
		page._send_data(page.driver, "id", loc_borrower['yjsr'], data['monthly_incoming'])  # 月均收入
		page.driver.find_element_by_css_selector("input[type=\"checkbox\"]").click()  # 是否有社保 Todo
		# 临时保存
		page.driver.find_element_by_css_selector(
				"#apply_module_apply_save > span.l-btn-left > span.l-btn-text > span.a_text").click()
		time.sleep(4)
		page.driver.find_element_by_xpath("html/body/div[2]/div[3]/a").click()
		time.sleep(1)
	
	if num == 1:
		action()
	elif num == 2:
		action()
	else:
		print "more than 2 borrower want to be input!"


# 业务基本信息- 输入物业信息(Basic business information-Property information)
def input_bbi_Property_info(page):
	# 这步骤很关键，没有选中，则定位不到下面的元素
	try:
		t1 = page.driver.find_element_by_class_name("house-head-line")
		t1.click()
		page.driver.execute_script("window.scrollTo(1600, 0)")  # 页面滑动到顶部
		page.driver.find_element_by_link_text(u"业务基本信息").click()
	except EC.ElementNotVisibleException as e:
		print e.msg
		raise e
	
	page.driver.find_element_by_name("propertyOwner").clear()
	page.driver.find_element_by_name("propertyOwner").send_keys("moban_gqt_test_1")  # 产权人
	page.driver.find_element_by_name("propertyNo").clear()
	page.driver.find_element_by_name("propertyNo").send_keys("gqt0132546")  # 房产证号
	
	# Todo
	time.sleep(3)
	page.driver.find_element_by_name("propertyStatus").click()  # 是否涉贷物业
	
	page.driver.find_element_by_name("propertyAge").click()
	page.driver.find_element_by_name("propertyAge").clear()
	page.driver.find_element_by_name("propertyAge").send_keys("10")  # 房龄
	
	page.driver.find_element_by_name("propertyArea").clear()
	page.driver.find_element_by_name("propertyArea").send_keys("100")  # 建筑面积
	
	page.driver.find_element_by_name("registrationPrice").clear()
	page.driver.find_element_by_name("registrationPrice").send_keys("200")  # 等级价
	
	# 地址
	Select(page.driver.find_element_by_name("propertyAddressProvince")).select_by_visible_text(u"河北省")
	Select(page.driver.find_element_by_name("propertyAddressCity")).select_by_visible_text(u"秦皇岛市")
	Select(page.driver.find_element_by_name("propertyAddressDistinct")).select_by_visible_text(u"山海关区")
	page.driver.find_element_by_id("propertyAddressDetail").clear()
	page.driver.find_element_by_id("propertyAddressDetail").send_keys(u"不知道在哪个地方")
	
	page.driver.find_element_by_name("evaluationSumAmount").clear()
	page.driver.find_element_by_name("evaluationSumAmount").send_keys("200")  # 评估公允价总值
	page.driver.find_element_by_name("evaluationNetAmount").clear()
	page.driver.find_element_by_name("evaluationNetAmount").send_keys("201")  # 评估公允价净值
	page.driver.find_element_by_name("slSumAmount").clear()
	page.driver.find_element_by_name("slSumAmount").send_keys("202")  # 世联评估总值
	page.driver.find_element_by_name("slPrice").clear()
	page.driver.find_element_by_name("slPrice").send_keys("203")  # 世联评估净值
	page.driver.find_element_by_name("agentSumAmout").clear()
	page.driver.find_element_by_name("agentSumAmout").send_keys("204")  # 中介评估总值
	page.driver.find_element_by_name("agentNetAmount").clear()
	page.driver.find_element_by_name("agentNetAmount").send_keys("205")  # 中介评估净值
	page.driver.find_element_by_name("netSumAmount").clear()
	page.driver.find_element_by_name("netSumAmount").send_keys("206")  # 网评总值
	page.driver.find_element_by_name("netAmount").clear()
	page.driver.find_element_by_name("netAmount").send_keys("207")  # 网评净值
	page.driver.find_element_by_name("localSumAmount").clear()
	page.driver.find_element_by_name("localSumAmount").send_keys("208")  # 当地评估总值
	page.driver.find_element_by_name("localNetValue").clear()
	page.driver.find_element_by_name("localNetValue").send_keys("209")  # 当地评估净值
	page.driver.find_element_by_name("remark").clear()
	page.driver.find_element_by_name("remark").send_keys(u"周边环境良好")  # 物业配套描述
	page.driver.find_element_by_name("localAssessmentOrigin").clear()
	page.driver.find_element_by_name("localAssessmentOrigin").send_keys(u"房产局")  # 当地评估来源
	page.driver.find_element_by_name("assessmentOrigin").clear()
	page.driver.find_element_by_name("assessmentOrigin").send_keys(u"房产局")  # 评估来源
	page.driver.find_element_by_name("evaluationCaseDescrip").click()
	page.driver.find_element_by_name("localAssessmentOrigin").clear()
	page.driver.find_element_by_name("localAssessmentOrigin").send_keys(u"世联行")
	
	page.driver.find_element_by_name("evaluationCaseDescrip").clear()
	page.driver.find_element_by_name("evaluationCaseDescrip").send_keys(u"符合事实")  # 评估情况描述
	
	# 征信信息
	page.driver.find_element_by_link_text(u"征信信息").click()
	page.driver.find_element_by_name("loanIdNum").clear()
	page.driver.find_element_by_name("loanIdNum").send_keys("moban_gqt_test_1")
	page.driver.find_element_by_name("creditOverdueNum").clear()
	page.driver.find_element_by_name("creditOverdueNum").send_keys("0")
	page.driver.find_element_by_name("queryLoanNum").clear()
	page.driver.find_element_by_name("queryLoanNum").send_keys("0")
	page.driver.find_element_by_name("loanOtherAmt").clear()
	page.driver.find_element_by_name("loanOtherAmt").send_keys("0")
	
	page.driver.find_element_by_link_text(u"网查信息").click()
	page.driver.find_element_by_class_name("remark").click()
	p1 = page.driver.find_element_by_xpath("//*[@id='apply_module_check_data_form']/div/div/textarea")
	p1.click()
	p1.send_keys(u"哈哈哈哈哈，无异常")
	
	page.driver.find_element_by_link_text(u"借款用途及回款来源").click()
	page.driver.find_element_by_id("apply_module_payment_source").send_keys(u"薪资回款")
	p2 = page.driver.find_element_by_xpath("//*[@id=\"apply_module_remark\"]")
	p2.click()
	p2.send_keys(u"无异常")
	
	page.driver.find_element_by_link_text(u"风控措施").click()
	page.driver.find_element_by_name("riskRemark").click()
	page.driver.find_element_by_name("riskRemark").send_keys(u"无异常")
	# 保存
	save(page)


# 申请件查询，获取applyCode
def get_applycode(page, condition):
	# 打开任务中心
	page._click_control(page.driver, "xpath", "html/body/header/ul/li[2]")
	# 申请件查询
	page.driver.find_element_by_xpath("/html/body/header/ul/li[2]/ul/li[4]").click()
	time.sleep(2)
	# 切换iframe 申请件查询
	page.driver.switch_to.frame("bTabs_tab_house_commonIndex_applySearch_index")
	# 打开表单
	time.sleep(2)
	page.driver.find_element_by_class_name("main-form-table").click()
	time.sleep(2)
	page.driver.find_element_by_xpath("//*[@id='row-content']/div[2]/input").click()
	# 根据条件查询录入案件
	page.driver.find_element_by_xpath("//*[@id='row-content']/div[2]/input").send_keys(unicode(condition))
	page.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/a[1]").click()
	t1 = page.driver.find_element_by_xpath("//*[@id='datagrid-row-r2-2-0']/td[9]")
	
	if t1:
		# 获取申请编号
		return t1.text
	else:
		return False


# 待处理任务查询
def query_task(page, condition):
	page.driver.switch_to.default_content()
	# 打开任务中心
	page._click_control(page.driver, "xpath", "html/body/header/ul/li[2]")
	time.sleep(1)
	# 待处理任务
	page.driver.find_element_by_xpath("/html/body/header/ul/li[2]/ul/li[2]").click()
	
	# 切换iframe 待处理任务
	page.driver.switch_to.frame("bTabs_tab_house_commonIndex_todoList")
	#  打开表单
	time.sleep(2)
	page.driver.find_element_by_id("frmQuery").click()
	# 选定申请编号搜索框
	page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").click()
	# 输入申请编号
	page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").send_keys(condition)
	# 点击查询按钮
	page.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/a[1]/span").click()
	t1 = page.driver.find_element_by_xpath("//*[@id='datagrid-row-r2-2-0']/td[9]")
	
	if not t1.text:
		return False
	else:
		return True


# 流程监控
def process_monitor(page, condition):
	page.driver.switch_to.default_content()
	# 打开任务中心
	page._click_control(page.driver, "xpath", "html/body/header/ul/li[2]")
	time.sleep(1)
	# 流程监控
	page.driver.find_element_by_xpath("/html/body/header/ul/li[2]/ul/li[1]").click()
	#  切换frame
	page.driver.switch_to.frame("bTabs_tab_house_commonIndex_processMonitor")
	time.sleep(1)
	# 输入搜索条件
	page.driver.find_element_by_name("process_search").click()
	time.sleep(1)
	page.driver.find_element_by_xpath("//*[@id='applyCode']").click()
	page.driver.find_element_by_xpath("//*[@id='applyCode']").send_keys(condition)
	time.sleep(1)
	# 点击查询
	page.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/a[1]/span").click()
	time.sleep(1)
	# 校验查询结果
	res = page.driver.find_element_by_xpath("//*[@id='datagrid-row-r4-2-0']/td[5]/div")
	time.sleep(2)
	if not res.text:
		return False
	else:
		res.click()
		page.driver.find_element_by_class_name("datagrid-btable").click()
		# 双击该笔案件
		ActionChains(page.driver).double_click(res).perform()
		time.sleep(1)
		res = page.driver.find_element_by_class_name("datagrid-btable")
		rcount = res.find_elements_by_tag_name("tr")  # 取表格的行数
		for i in range(1, len(rcount)):
			text = page.driver.find_element_by_xpath('//*[@id="datagrid-row-r1-2-%s"]/td[1]/div' % i).text
			time.sleep(1)
			print text  # 返回节点所有值
		# 下一步处理人ID
		next_user_id = page.driver.find_element_by_xpath(
				'//*[@id="datagrid-row-r1-2-%s"]/td[4]/div' % (len(rcount) - 1)).text
		print "next_user_id:" + next_user_id
		return next_user_id


# 申请录入保存
def save(page):
	page.driver.find_element_by_css_selector(
			"#apply_module_apply_save > span.l-btn-left > span.l-btn-text > span.a_text").click()
	time.sleep(1)
	# 弹窗关闭
	page.driver.find_element_by_xpath("html/body/div[2]/div[3]/a").click()  # 确认保存
	time.sleep(1)


# 申请录入提交
def submit(page):
	page.driver.find_element_by_id("apply_module_apply_submit").click()
	page.driver.find_element_by_xpath("html/body/div[2]/div[3]/a").click()


# 分公司主管批审核
def branch_supervisor_approval(page, condition):
	# 打开任务中心
	page._click_control(page.driver, "xpath", "html/body/header/ul/li[2]")
	time.sleep(1)
	# 待处理任务
	page.driver.find_element_by_xpath("/html/body/header/ul/li[2]/ul/li[2]").click()
	time.sleep(2)
	# 切换iframe 待处理任务
	page.driver.switch_to.frame("bTabs_tab_house_commonIndex_todoList")
	#  打开表单
	time.sleep(1)
	page.driver.find_element_by_id("frmQuery").click()
	# 选定申请编号搜索框
	page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").click()
	# 输入申请编号
	time.sleep(1)
	page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").send_keys(condition)
	# page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").send_keys("GZ20171116C05")
	# 点击查询按钮
	page.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/a[1]/span").click()
	time.sleep(1)
	t1 = page.driver.find_element_by_xpath("//*[@id='datagrid-row-r2-2-0']/td[3]")
	time.sleep(1)
	if not t1.text:
		return False
	else:
		t1.click()
		page.driver.find_element_by_class_name("datagrid-btable").click()
		# 双击该笔案件
		ActionChains(page.driver).double_click(t1).perform()
		time.sleep(1)
		# 填写批核意见
		page.driver.find_element_by_class_name("container-fluid").click()
		page.driver.find_element_by_xpath("//*[@id=\"approve_opinion_form\"]/div[5]/div[2]").click()
		page.driver.find_element_by_xpath("//*[@id=\"remarkable\"]").send_keys(u"分公司主管同意审批")
		
		# 保存
		page.driver.find_element_by_xpath("//*[@id=\"apply_module_apply_save\"]/span/span/span[2]").click()
		time.sleep(1)
		page.driver.find_element_by_xpath("/html/body/div[5]/div[3]/a/span/span").click()  # 关闭弹窗
		
		# 提交
		page.driver.find_element_by_xpath("//*[@id='apply_module_apply_submit']/span/span/span[2]").click()
		time.sleep(2)
		page.driver.find_element_by_xpath("/html/body/div[5]/div[3]/a").click()


# 分公司经理审批
def branch_manager_approval(page, condition):
	# 打开任务中心
	page._click_control(page.driver, "xpath", "html/body/header/ul/li[2]")
	time.sleep(1)
	# 待处理任务
	page.driver.find_element_by_xpath("/html/body/header/ul/li[2]/ul/li[2]").click()
	time.sleep(2)
	# 切换iframe 待处理任务
	page.driver.switch_to.frame("bTabs_tab_house_commonIndex_todoList")
	#  打开表单
	time.sleep(1)
	page.driver.find_element_by_id("frmQuery").click()
	# 选定申请编号搜索框
	page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").click()
	# 输入申请编号
	time.sleep(1)
	page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").send_keys(condition)
	# page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").send_keys("GZ20171116C05")
	# 点击查询按钮
	page.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/a[1]/span").click()
	time.sleep(1)
	t1 = page.driver.find_element_by_xpath("//*[@id='datagrid-row-r2-2-0']/td[3]")
	time.sleep(1)
	if not t1.text:
		return False
	else:
		t1.click()
		page.driver.find_element_by_class_name("datagrid-btable").click()
		# 双击该笔案件
		ActionChains(page.driver).double_click(t1).perform()
		time.sleep(1)
		# 填写批核意见
		page.driver.find_element_by_class_name("container-fluid").click()
		page.driver.find_element_by_xpath("//*[@id=\"approve_opinion_form\"]/div[5]/div[2]").click()
		page.driver.find_element_by_xpath("//*[@id=\"remarkable\"]").send_keys(u"分公司经理同意审批")
		
		# 保存
		page.driver.find_element_by_xpath("//*[@id=\"apply_module_apply_save\"]/span/span/span[2]").click()
		time.sleep(1)
		page.driver.find_element_by_xpath("/html/body/div[5]/div[3]/a/span/span").click()  # 关闭弹窗
		
		# 提交
		page.driver.find_element_by_xpath("//*[@id='apply_module_apply_submit']/span/span/span[2]").click()
		time.sleep(2)
		page.driver.find_element_by_xpath("/html/body/div[5]/div[3]/a").click()


# 区域预复核
def regional_prereview(page, condition):
	# 打开任务中心
	page._click_control(page.driver, "xpath", "html/body/header/ul/li[2]")
	time.sleep(1)
	# 待处理任务
	page.driver.find_element_by_xpath("/html/body/header/ul/li[2]/ul/li[2]").click()
	time.sleep(2)
	# 切换iframe 待处理任务
	page.driver.switch_to.frame("bTabs_tab_house_commonIndex_todoList")
	#  打开表单
	time.sleep(1)
	page.driver.find_element_by_id("frmQuery").click()
	# 选定申请编号搜索框
	page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").click()
	# 输入申请编号
	time.sleep(1)
	page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").send_keys(condition)
	# page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").send_keys("GZ20171116C05")
	# 点击查询按钮
	page.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/a[1]/span").click()
	time.sleep(1)
	t1 = page.driver.find_element_by_xpath("//*[@id='datagrid-row-r2-2-0']/td[3]")
	time.sleep(1)
	if not t1.text:
		return False
	else:
		t1.click()
		page.driver.find_element_by_class_name("datagrid-btable").click()
		# 双击该笔案件
		ActionChains(page.driver).double_click(t1).perform()
		time.sleep(1)
		# 填写批核意见
		page.driver.find_element_by_class_name("container-fluid").click()
		page.driver.find_element_by_xpath("//*[@id=\"approve_opinion_form\"]/div[5]/div[2]").click()
		page.driver.find_element_by_xpath("//*[@id=\"remarkable\"]").send_keys(u"区域预复核")
		
		# 保存
		page.driver.find_element_by_xpath("//*[@id=\"apply_module_apply_save\"]/span/span/span[2]").click()
		time.sleep(1)
		page.driver.find_element_by_xpath("/html/body/div[5]/div[3]/a/span/span").click()  # 关闭弹窗
		
		# 提交
		page.driver.find_element_by_xpath("//*[@id='apply_module_apply_submit']/span/span/span[2]").click()
		time.sleep(2)
		page.driver.find_element_by_xpath("/html/body/div[5]/div[3]/a").click()
