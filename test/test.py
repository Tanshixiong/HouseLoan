# coding:utf-8

import time

from selenium import webdriver

driver = webdriver.Chrome()
driver.get("http://10.15.14.48:8098/app/login")
driver.find_element_by_name("j_username").clear()
driver.find_element_by_name("j_password").clear()
driver.find_element_by_name("j_username").send_keys("xn044665")
driver.find_element_by_name("j_password").send_keys("111111")
driver.find_element_by_css_selector("input.login-btn").click()

time.sleep(2)
driver.find_element_by_xpath("html/body/header/ul/li[3]").click()
time.sleep(2)
driver.find_element_by_xpath("html/body/header/ul/li[3]/ul/li[1]/a").click()
driver.switch_to.frame("framing")
driver.find_element_by_xpath(".//*[@id='nav-tabs']/li[2]/a").click()

if __name__ == '__main__':
	main()
