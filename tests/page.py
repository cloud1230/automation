# -*- coding:utf-8 -*-  
import time
import abc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import testdata
from locators import *

class BasePage(object):
	def __init__(self, driver):
		self.driver = driver

	def wait_element(self, locator):
		try:
			WebDriverWait(self.driver, 100).until(
			EC.presence_of_element_located(locator))
			return True
		except:
			print "Exception: Wait element failed to find element..."
			return False

	def loop_wait_and_refresh(self, locator, times):
		for i in range(times):
			if self.wait_element(locator):
				break
			else:
				self.driver.refresh()
				time.sleep(10)

	@abc.abstractmethod
	def _validate_page(self):
		return

	def enter_textfield(self, locator, text):
		self.loop_wait_and_refresh(locator, testdata.LOOP_REFRESH_TIMES)
		self.driver.find_element(*locator).send_keys(text)


class LoginPage(BasePage):
	def __init__(self, driver):
		super(LoginPage, self).__init__(driver)
		self.username = LoginPageLocators.USERNAME
		self.password = LoginPageLocators.PASSWORD
		self.submit = LoginPageLocators.SUBMIT_BUTTON

	def _validate_page(self):
		if not testdata.LOGIN_TITLE in self.driver.title:
			raise Exception("Invalid page : LoginPage")

	def set_username_and_password(self, username, password):
		self.enter_textfield(self.username, username)
		self.enter_textfield(self.password, password)

	def click_submit_button(self):
		submit_button = self.driver.find_element(*self.submit)
		submit_button.click()
