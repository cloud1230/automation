import threading
import time
import logging
import sys

from common.database_wrapper import *
from common.logger import *
from common.constants import *
from common.utility import *
from tests.webtest.BVTTestCases import *

class TaskExecutionEngine(threading.Thread):
	def __init__(self, lock, thread_name):
		super(TaskExecutionEngine, self).__init__(name = thread_name)
		self.lock = lock
		self.name = thread_name
		self.setDaemon(True)

	def run(self):
		self.lock.acquire()
		all_tasks = []
		task = OperateMySQL().get_scheduled_task(TASK_STATUS['Sch'])
		if not task:
			print "\b."
			return

		print '##################################task: ', task
		scen_logger = TestScenarioLog()
		scen_logger.initialize(task)

		self.lock.release()

		if scen_logger['bused']:
			self.run_scheduled_task(task, scen_logger)

	def run_scheduled_task(self, task, scen_logger):
		if task[1] == 'bvt':
			print 'Running java agent bvt related tasks...'
			BVTTestRun(scen_logger).run()

		elif task[1] == 'regression':
			print 'Running java agent regresion related tasks...'
			InstallRegressionTestRun(scen_logger).run()

		elif task[1] == 'database':
			print 'Running java agent database regresion related tasks...'
			InstallRegressionTestRun(scen_logger).run()

		else:
			raise Exception("Unknown java agent test type: %s specified in the task!" % task[1])
			update_test_status(task[0], TASK_STATUS['Cal'])

					
if __name__=='__main__':
	MAX_THREAD = 5
	logging.setLoggerClass(TestLog)
	checkLoggingMultiThreading()

	while True:
		try:
			for i in range(5):
				if threading.activeCount() < MAX_THREAD:
					TaskExecutionEngine(threading.Lock(), '-1.-1').start()
				time.sleep(60)

			print "%d:%d " % (threading.activeCount(),MAX_THREAD)
		except Exception,e:
			getLog().Error("Test engine exception: " + str(e))
			time.sleep(60)