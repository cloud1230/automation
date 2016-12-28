import time
import os
from selenium import webdriver
#print selenium.__file__
import page
import testdata
import sys
sys.path.append('..')
import common.constants

DRIVERS = {
	'firefox':lambda:webdriver.Firefox(
		executable_path=os.path.join(common.constants.BASE_DIR, 'tests/drivers/geckodriver')),
	'chrome' :lambda:webdriver.Chrome(),
	'ie':lambda:webdriver.Ie(),
	'opera': lambda:webdriver.Opera(),
	}

class Operator(object):
	def __init__(self, url, driver_type):
		try:
			self.driver = DRIVERS[driver_type]()
			#self.driver.maximize_window()
			self.url = url
			#open the browser
			self.driver.get(self.url)
			#page initialization
			self.login_page = page.LoginPage(self.driver)

		except Exception, e:
			print "Operator initialization exception!", str(e)

	def get_driver(self):
		return self.driver

	def get_file_folder(self):
		current_day_str = time.strftime("%Y%m%d")
		day_folder = os.path.join(common.constants.SNAPSHOT_FOLDER, current_day_str)
		if not os.path.exists(day_folder):
			os.makedirs(day_folder)

		return current_day_str, day_folder

	def take_snapshot(self):
		current_day_str, day_folder = self.get_file_folder()

		file_name = "screenshot"+time.strftime("%Y%m%d%H%M%S")+".png"
		file_path = os.path.join(day_folder, file_name)
		time.sleep(3)
		self.driver.save_screenshot(file_path)
		
		snapshot_url = "http://%s:%s/%s/%s" % (common.constants.HOST, common.constants.LOG_PORT, current_day_str, file_name)

		return snapshot_url  

	def save_log(self, path):
		current_day_str, day_folder = self.get_file_folder()

		file_name = path.split('/')[-1]

		try:
			os.system("cp %s %s" % (path, day_folder))
		except Exception,e:
			print "Save log exception: ", str(e)

		#if os.path.isfile(os.path.join(day_folder, file_name)):
		log_url = "http://%s:%s/%s/%s" % (common.constants.HOST, common.constants.LOG_PORT, current_day_str, file_name)

		return log_url

	def finalize(self):
		self.driver.quit()

	@staticmethod
	def get_other_log_download_path(driver_type, log_path):
		operator = Operator('http://127.0.0.1', driver_type)
		snapshot_path = operator.save_log(log_path)
		operator.finalize()

		return snapshot_path

if __name__ == '__main__':
	get_other_log_download_path('firefox', 'geckodriver.log')
	#pass