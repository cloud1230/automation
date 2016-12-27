import os
import logging
import datetime
import threading
import time
import constants
from utility import *
from database_wrapper import *
from email_report import *

class TestLog(logging.getLoggerClass()):
	def __init__(self, sName=''):
		logging.Logger.__init__(self, sName)
		if (sName == '-1'):
			sName = 'webautomation'

		sPath = os.path.join(constants.BASE_DIR, 'logs')
		
		if not os.path.isdir(sPath):
			os.makedirs(sPath)

		sFile=os.path.join(sPath, '%s.log' % sName)
		
		if not os.path.isfile(sFile):
			os.system("touch {0}".format(sFile))
			os.system("chmod 775 {0}".format(sFile))

		logfile=logging.FileHandler(sFile)
		console=logging.StreamHandler()

		#self.setLevel(logging.NOTSET)
		self.level = 10
		logfile.setLevel(10)
		logfile.setLevel(10)

		logfile.setFormatter(logging.Formatter('%(levelname)s:%(message)s %(asctime)s')  )   
		console.setFormatter(logging.Formatter('%(levelname)s:%(message)s')  )

		self.addHandler(logfile)
		self.addHandler(console)

	def get_testcase_id (self):     
 		sName =  threading.currentThread().getName()
 		lNames = sName.split(".")
 		iBQID = -1
 		iTestcaseID = -1
 		iLen = len(lNames)
        
		try:
			iBQID =     int(lNames[0])
			iTestcaseID = int(lNames[1])
		except:
			pass

		return (iBQID, iTestcaseID)

	def getNowTime(self):
		now=datetime.datetime.now()
		return "{0}-{1}-{2} {3}:{4}:{5}".format(now.year,now.month,now.day,now.hour,now.minute,now.second)

	def Pass(self,sInfo, attachment=''):
		self.info("PASS: {0} {1}".format(sInfo,self.getNowTime()))
		iBQID, iTestcaseID = self.get_testcase_id()
		log_content = sInfo + " " + self.getNowTime()
		OperateMySQL().output_test_case_log(iTestcaseID, 'PASS', self.handler_msg_before_database(log_content), attachment)

	def Warn(self,sInfo, attachment=''):
		self.info("WARN: {0} {1}".format(sInfo,self.getNowTime()))
		iBQID, iTestcaseID = self.get_testcase_id()
		log_content = sInfo + " " + self.getNowTime()
		OperateMySQL().output_test_case_log(iTestcaseID, 'WARN', self.handler_msg_before_database(log_content), attachment)

	def Error(self,sInfo, attachment=''):
		self.error("{0} {1}".format(sInfo,self.getNowTime()))
		iBQID, iTestcaseID = self.get_testcase_id()
		log_content = sInfo + " " + self.getNowTime()
		OperateMySQL().output_test_case_log(iTestcaseID, 'ERROR', self.handler_msg_before_database(log_content), attachment)

	def Message(self,sInfo, attachment=''):
		self.info("{0} {1}".format(sInfo,self.getNowTime()))
		iBQID, iTestcaseID = self.get_testcase_id()
		log_content = sInfo + " " + self.getNowTime()
		OperateMySQL().output_test_case_log(iTestcaseID, 'INFO', log_content, attachment)

	def Fail(self,sInfo, attachment=''):
		self.error("FAIL: {0} {1}".format(sInfo,self.getNowTime()))
		iBQID, iTestcaseID = self.get_testcase_id()
		log_content = sInfo + " " + self.getNowTime()
		OperateMySQL().output_test_case_log(iTestcaseID, 'FAIL', self.handler_msg_before_database(log_content), attachment)

	def handler_msg_before_database(self, msg):
		content = msg.replace('\'', '').replace('\"', '').replace("'","")
		return content	

def checkLoggingMultiThreading ():
	if hasattr(logging, 'multiprocessing'):
		pass
	else:
		print "Setting multiprocessing for logging module"
		try:
			logging._acquireLock()
			OldLoggerClass = logging.getLoggerClass()
			if not getattr(OldLoggerClass, '_process_aware', False):
				class ProcessAwareLogger(OldLoggerClass):
					_process_aware = True
					def makeRecord(self, *args, **kwds):
						record = OldLoggerClass.makeRecord(self, *args, **kwds)
						record.processName = threading.currentThread().getName()
						return record
				logging.setLoggerClass(ProcessAwareLogger)
		finally:           
			logging._releaseLock()

def getLog():
	sName =  threading.currentThread().getName()
	#print "get log function thread name : %s" % sName
	lNames = sName.split(".")
	iBQID = -1
	iTestcaseID = -1
	iLen = len(lNames)

	try:
		iBQID =     int(lNames[0])
		iTestcaseID = int(lNames[1])
	except:
		pass
	finally:

		return logging.getLogger("%d" % iBQID)

class TestScenarioLog(UserDict):
	def __init__(self):
		UserDict.__init__(self)

		self['sid'] = -1
		self['task_id'] = -1
		self['project'] = ''
		self['test_type'] = ''
		self['browser'] = 0
		self['description'] = ''
		self['user'] = ''
		self['task'] = ''
		self['created'] = ''
		self['build_info'] = ''

		self.Builds = {}

		self['bused'] = False
		self['bServer'] = False
		self['server_container'] = ''
		self.configs = []
		self['bpassed'] = False
		self['pass'] = -1
		self['fail'] = -1
		self['agent_log_path'] = ''
		self['collector_log_path'] = ''

	def initialize(self, task):
		self['task'] = task
		self['sid'] = task[0]
		self['project'] = task[3]
		self['test_type'] = task[1]
		self['user'] = task[4]
		self['description'] = task[7]
		self['browser'] = task[5]
		self['created'] = task[8]
		self['build_info'] = task[6]
		self['updated'] = task[9]

		lproducts = self['build_info'].split(';')

		for builds in lproducts:
			stype = builds.split(':')[0]
			sversion = builds.split(':')[1]
			spath = builds.split(':')[2]
			if 'server' in stype:
				self.Builds['server'] = [stype, sversion, spath]
			elif 'java' in stype:
				self.Builds['javaagent'] = [stype, sversion, spath]
			else:
				raise Exception("Unexpected type %s parsed from database build info field." % self.stype)

		try :
			if self.Builds['server']:
				self['bServer'] = True
		except:
			print "This test scentario doesn't contain a server. Will creating for it."

		if ',' in self['config_id']:
			self.handle_multiple_configs()

		else:
			xml_files_folder = os.path.join(BASE_DIR, 'docker_configs', self['project'], self['test_type'], str(self['config_id']))
	
			xml_configs = get_config_list(xml_files_folder)
			
			for xml_config in xml_configs:
				if self['bServer']:
					if xml_config['server'] and self.Builds['server'][2] not in xml_config['files']:
						xml_config['files'].append(self.Builds['server'][2])
						xml_config['scripts'].append({'path':os.path.join(BASE_DIR, 'configurations/server', 'install_tps_server.py'), 'args':[]})
						self['server_container'] = xml_config['container_name']
						self.configs.insert(0, xml_config)

				if xml_config['agent'] and self.Builds['javaagent'][2] not in xml_config['files']:
					xml_config['files'].append(self.Builds['javaagent'][2])
					xml_config['scripts'].append({'path':os.path.join(BASE_DIR, 'configurations/bvtdemo', 'install_agent.py'),'args':[]})
					#xml_config['scripts'].append({'path':os.path.join(BASE_DIR, 'configurations/bvtdemo', 'install_agent.py'),'args':[]})
					self.configs.append(xml_config)

		# add server_container to agent config
			for i in range(len(self.configs)):
				if self.configs[i]['agent']:
					self.configs[i]['server_container'] = self['server_container']

			update_test_run_status = OperateMySQL(UpdateTestRunStatus)
			update_test_run_status.operate_query(sid=self['sid'], status=TASK_STATUS["Run"])
			self['bused'] = True

	def handle_multiple_configs(self):
		# delete current row in db
		# insert to current db with multiple rows with same summary_desc but different with other times
		config_id_list = self['config_id'].split(',')
		current_running = ";current_running_"+time.strftime("%Y%m%d%H%M%S")

		for config_id in config_id_list:
			new_test_run = OperateMySQL(NewTestRun)
			new_test_run.operate_query(
				test_type = self['test_type'], 
				config_id = config_id.strip(),
				test_status = "Scheduled", 
				proj_name = self['project'], 
				user_name = self['user'], 
				summary_desc = self['description']+current_running, 
				build_info =  self['build_info']
				)
		OperateMySQL().delete_multiple_config_record(self['sid'])
		self['bused'] = False

	def finalize(self):
		update_test_run_status = OperateMySQL(UpdateTestRunStatus)
		update_test_run_status.operate_query(sid=self['sid'], status=TASK_STATUS["Fin"])

		if self['project'] == 'javaagent' and self['test_type'] == 'bvt':
			self.send_javaagent_email_report()
		elif self['project'] == 'javaagent' and self['test_type'] == 'regression':
			self.send_javaagent_regression_email_report()
		elif self['project'] == 'javaagent' and self['test_type'] == 'database':
			self.send_javaagent_regression_email_report()

	def send_javaagent_email_report(self):
		self['bpassed'], self['fail'], self['pass'] = OperateMySQL().get_task_test_result(self['sid'])
		print "fail: %d, pass: %d" % (self['fail'], self['pass'])
		for config in self.configs:
			if config['server']:
				server_addr = get_tps_server_url(config)
				print "server address:", server_addr
			elif config['agent']:
				demo_addr = get_bvt_demo_url(config)
				print "demo address:", demo_addr

		#email_rows = []
		#SID	ProductConfig IDTest TypePassFailTotalPassPercentStart Time
		end_time = OperateMySQL().get_bvt_task_end_time(self['sid'])
		row_content = [
			str(self['sid']), 
			self['project'], 
			self['config_id'], 
			self['test_type'],
			str(self['pass']),
			str(self['fail']),
			self['pass']+self['fail'],
			"{:.0%}".format(float(self['pass'])/(self['pass']+self['fail'])),
			#"100%",
			str(self['created']),
			end_time
			]

		builds = "tps_server_version:%s;java_agent_version:%s" % (self.Builds['server'][1], self.Builds['javaagent'][1])
		bvt_mail = EmailReportBuilder(builds)
		formated_msg = bvt_mail.get_bvt_email_html_text(server_addr, demo_addr, row_content, self['bpassed'])

		if self['bpassed']:
			subject = "Succeeded: Your %s Test of %s(config: %s) has completed!" % (self['test_type'], self['project'], self['config_id'])
		else:
			subject = "Failed: Your %s Test of %s(config: %s) has completed!" % (self['test_type'], self['project'], self['config_id'])

		#if self['user'] != '':
		bvt_mail.send_report(subject, formated_msg, to=JAVA_AGENT_TO_LIST)

	def send_javaagent_regression_email_report(self):
		
		if len(self['description'].split(';')) > 1:
			fixed_value = self['description'].split(';')[-1].strip()

			sid_list, configid_list, created_list, updated_list = OperateMySQL().get_configs_using_fixed_value(fixed_value)

			rows = []
			bpassed_list = []

			#waiting = True
			#while waiting:
			status_list = []
			for sid_number in sid_list:
				status_list.append(OperateMySQL().get_test_status_by_sid(sid_number))
				
			if status_list.count('Finished') == len(sid_list):
			#			waiting = False
			#	time.sleep(60*5)

#			if max(sid_list) == self['sid']:
				for item in sid_list:
					bpassed, failed, passed = OperateMySQL().get_task_test_result(item)
					index_number = sid_list.index(item)

					row_content = [
						str(item), 
						self['project'], 
						configid_list[index_number], 
						self['test_type'],
						str(passed),
						str(failed),
						passed+failed,
						"{:.0%}".format(float(passed)/(passed+failed)),
						#"100%",
						created_list[index_number],
						updated_list[index_number]
						]
					bpassed_list.append(bpassed)
					rows.append(row_content)

				builds = "tps_server_version:%s;java_agent_version:%s" % (self.Builds['server'][1], self.Builds['javaagent'][1])
				regression_mail = EmailReportBuilder(builds)
				formated_msg = regression_mail.get_regression_email_html_text(rows, bpassed_list)

				config_ids = ','.join(configid_list)
				if False in bpassed_list:
					subject = "Faled: Your %s Test of %s(config(s): %s) has completed!" % (self['test_type'], self['project'], config_ids)
				else:
					subject = "Succeeded: Your %s Test of %s(config(s): %s) has completed!" % (self['test_type'], self['project'], config_ids)

				#if self['user'] != '':
				regression_mail.send_report(subject, formated_msg, to=JAVA_AGENT_TO_LIST)
				clean_for_spaces()
		else:
			self.send_javaagent_email_report()

class TestcaseLog(UserDict):
	def __init__(self):
		UserDict.__init__(self)
		self['task_id'] = -1
		self['sid'] = -1
		self['task_name'] = ''
		self['task_desc'] = ''
		self['pass'] = 0
		self['fail'] = 0
		self['error'] = 0

	def initialize(self, sid, task_name, task_desc):
		self['sid'] = sid
		self['task_name'] = task_name
		self['task_desc'] = task_desc

		self['task_id'] = OperateMySQL().initiallize_test_case(self['sid'], self['task_name'], self['task_desc'])

		threading.currentThread().setName("%d.%d" % (self['sid'], self['task_id']))

		getLog().Message("Test case (Name: %s, ID: %d, SID: %d) was initialized." % (self['task_name'], self['task_id'], self['sid']))

	def finalize(self):
		bPass, fail_result, error_result = OperateMySQL().get_task_detail_test_result(self['task_id'])
		if bPass:
			OperateMySQL().update_test_case_result(self['task_id'], 'PASS')
			getLog().Pass("Test case (Name: %s, ID: %d, SID: %d) running successfully." % (self['task_name'], self['task_id'], self['sid']))
		else:
			OperateMySQL().update_test_case_result(self['task_id'], 'FAIL')
			getLog().Fail("Test case (Name: %s, ID: %d, SID: %d) running failed." % (self['task_name'], self['task_id'], self['sid']))

		getLog().Message("Test case (Name: %s, ID: %d, SID: %d) is finalized." % (self['task_name'], self['task_id'], self['sid']))


if __name__=="__main__":

	testcaselogger = TestcaseLog()
	testcaselogger.initialize(1, "setup", "setup dockler")
	testcaselogger.finalize()



