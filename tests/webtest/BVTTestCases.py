import time
import os
from UserDict import UserDict
from functools import wraps
import sys
sys.path.append('tests')
import testdata
import operators
from test_decorators import *
sys.path.append('../..')
from common.logger import *

class InstallBVTTestRun(UserDict):
	def __init__(self, scen_logger):
		UserDict.__init__(self)
		
		self.scen_logger = scen_logger
		self.test_case_logger = TestcaseLog()
		self.demo_run_times = 10
		self.force_stop = False
		self.debug = False

	def set_debug_status(self, debug):
		self.debug = debug

	def run(self):
		try:
			if self.scen_logger['sid'] == -1:
				raise Exception("Initializing sid of log DB failed!")
# all tests added here
			self.test_login()

		except Exception,e:
			#error = handler_msg_before_database(str(e))
			getLog().Error("Exception throwed from bvt test case, test ends up." + str(e))
		finally:
			#self.test_config_cleanup()
			self.scen_logger.finalize()

	@testcase('003_TestLogin', 'Verify we can correctly login tps server.')
	def test_login(self):
		getLog().Message("TPS server url is %s and use browser %s to browse the server." % (testdata.SERVER_URL, self.scen_logger['browser']))
		tps_operator = operators.Operator(testdata.SERVER_URL, self.scen_logger['browser'])
		getLog().Message("Set username: %s and password: %s then click submit button on TPS login page." % (testdata.tps_server_user, testdata.tps_server_password))
		tps_operator.login_page.set_username_and_password(testdata.tps_server_user, testdata.tps_server_password)
		getLog().Message("Click submit button to login.")
		tps_operator.login_page.click_submit_button()
		snapshot_path = tps_operator.take_snapshot()
		getLog().Message("Get login snapshot: ", snapshot_path)
		
		if testdata.LOGIN_TITLE in tps_operator.get_driver().title:
			getLog().Pass("Successfully Login.")
		else:
			getLog().Fail("Failed to Login.")

		getLog().Message("Close browser...")
		tps_operator.finalize()