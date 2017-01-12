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

class BaseTestRun(UserDict):
	def __init__(self, scen_logger):
		UserDict.__init__(self)
		self.testname = ''
		self.scen_logger = scen_logger
		self.test_case_logger = TestcaseLog()
		self.demo_run_times = 10
		self.force_stop = False
		self.debug = False

	def set_debug_status(self, debug):
		self.debug = debug

	def run():
		try:
			if self.scen_logger['sid'] == -1:
				raise Exception("Initializing sid of log DB failed!")
			
			pass

		except Exception,e:
			#error = handler_msg_before_database(str(e))
			getLog().Error("Exception throwed from bvt test case, test ends up." + str(e))
		finally:
			self.scen_logger.finalize()