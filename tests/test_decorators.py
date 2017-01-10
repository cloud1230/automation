import sys
sys.path.append('..')
from common.exceptions import *
from common.logger import *

def testcase(testname, test_desc):
	def _testcase(func):
		def wrapper(*args):
			try:
				self = args[0]
				self.test_case_logger.initialize(self.scen_logger['sid'], testname, test_desc)
				if self.force_stop:
					raise SkipTestException("Exiting text case %s for critical issues......" % testname)
				func(*args)
				
			except SkipTestException, e:
				self.force_stop = True
				getLog().Error(e.error)

			except Exception, e:
				self.force_stop = True
				getLog().Error(testname+': '+ str(e))

			finally:
				self.test_case_logger.finalize()
		return wrapper
	return _testcase