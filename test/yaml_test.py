# -*- coding:utf-8 -*-
import os
import yaml

current_path = os.path.abspath(os.path.dirname(__file__))
print(current_path)

with open('E:\HouseLoanAuto\config\\read_yaml.yaml', 'r') as f:
	temp = yaml.load(f.read())
	print(temp)
	print(temp['basic_name'])
	print(temp['basic_name']['test_name'])
	print(temp['basic_name']['selected_name'][0])
	lg = len(temp['basic_name']['selected_name'])
	for i in range(lg):
		print(temp['basic_name']['selected_name'][i])
	
	print(temp['cwd'][0])
