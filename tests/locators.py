# -*- coding:utf-8 -*-  

from selenium.webdriver.common.by import By

class BaseLocators(object):
	pass

class LoginPageLocators(BaseLocators):
	USERNAME = (By.NAME, "username")
	PASSWORD = (By.ID, "password")
	SUBMIT_BUTTON = (By.XPATH, "//*[@class='input-btn']")