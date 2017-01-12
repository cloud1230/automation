from BaseTestCases import *

class BVTTestRun(BaseTestRun):

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
			self.scen_logger.finalize()

	@testcase('003_TestLogin', 'Verify we can correctly login tps server.')
	def test_login(self):
		try:
			if self.force_stop:
					raise SkipTestException("Exiting text case %s for critical issues......" % self.testname)

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

		except SkipTestException, e:
			self.force_stop = True
			getLog().Error(e.error)

		except Exception, e:
			self.force_stop = True
			getLog().Error(self.testname+': '+ str(e))