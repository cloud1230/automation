import sys
sys.path.append('..')
from common.exceptions import *
#from common.logger import *

def testcase(testname, test_desc):
	def _testcase(func):
		def wrapper(*args):
			try:
				self = args[0]
				self.testname = testname
				self.test_case_logger.initialize(self.scen_logger['sid'], testname, test_desc)
				func(*args)		
				self.test_case_logger.finalize()
		return wrapper
	return _testcase