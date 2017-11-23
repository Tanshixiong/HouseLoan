# coding:utf-8

"""
根据table的id属性和table中的某一个元素定位其在table中的位置
table包括表头，位置坐标都是从1开始算
tableId：table的id属性
queryContent：需要确定位置的内容
"""


def get_table_content(driver, tableId, queryContent):
	# 按行查询表格的数据，取出的数据是一整行，按空格分隔每一列的数据
	# table_tr_list = driver.find_element(By.ID, tableId).find_elements(By.TAG_NAME, "tr")
	table_tr_list = driver.find_element_by_id(tableId).page.driver.find_element_by_tag_name("tr")
	
	table_list = []  # 存放table数据
	for tr in table_tr_list:  # 遍历每一个tr
		# 将每一个tr的数据根据td查询出来，返回结果为list对象
		# table_td_list = tr.find_elements(By.TAG_NAME, "td")
		table_td_list = tr.find_element_by_tag_name("td")
		row_list = []
		print(table_td_list)
		for td in table_td_list:  # 遍历每一个td
			row_list.append(td.text)  # 取出表格的数据，并放入行列表里
		table_list.append(row_list)
	
	# 循环遍历table数据，确定查询数据的位置
	for i in range(len(table_list)):
		for j in range(len(table_list[i])):
			if queryContent == table_list[i][j]:
				print("%r坐标为(%r,%r)" % (queryContent, i + 1, j + 1))


get_table_content(page.driver, "datagrid-btable", "第二行第二列")
