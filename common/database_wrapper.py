# -*- coding: UTF-8 -*-

import time
import MySQLdb
from logger import *
from UserDict import UserDict
import constants

class MySQLConnector(UserDict):
	def __init__(self):
		UserDict.__init__(self)

		self.db_conn = None
		self.db_cursor = None

		self["host"] = constants.LOG_DB_SERVER
		self["user"] = constants.LOG_DB_USER
		self["password"] = constants.LOG_DB_PASS
		self["database"] = constants.LOG_DATABASE
		self["port"] = constants.LOG_DB_PORT

	def connect(self):
		try:
			self.db_conn = MySQLdb.connect(self['host'], self["user"], self['password'], self['database'], self['port'])
			self.db_cursor = self.db_conn.cursor()
			return 0
		except Exception,e:
			print "Unable to open the database %s on %s.\n Exception: %s ...\n" % (self["database"], self["host"], str(e))
			print "Check the privileges connection..."
			return -1

	def disconnect(self):
		try:
			if self.db_cursor is not None:
				self.db_cursor.close()
			if self.db_conn is not None:
				self.db_conn.close()
		except Exception,e:
			print "Close the db connection: %s ..." % str(e)


class OperateMySQL(MySQLConnector):

	def __init__(self,strategy=None):
		MySQLConnector.__init__(self)
		if self.connect() == -1:
			raise Exception ("Failed to connect to database server . ")

		self.action = None
		if strategy:
			self.action = strategy()

	def operate_query(self, **kwargs):
		result = None
		if self.action:
			query_type, query = self.action.get_query(**kwargs)
			try:
				self.db_cursor.execute(query)

				if query_type == "insert":
					self.db_conn.commit()
					result = 0

				elif query_type == "selectone":
					rs = self.db_cursor.fetchone()
					if rs:
						result, = rs
				
				elif query_type == "selectlist":
					result=[]
					rs = self.db_cursor.fetchall()
					if rs:
						for item in rs:
							#sid, = item
							result.append(item)
			except Exception,e:
				print "Class %s has exception: " % str(self.action) + str(e)
			finally:
				self.disconnect()
			return result
		else:
			raise Exception("Exception raised, no strategyClass supplied to OperateMySQL class!")

	def get_task_detail_test_result(self, task_id):
		bpassed = False
		try:
			query = "select count(message_type) from reporting_taskdetail where task_id_id=%s and message_type='FAIL'" % task_id
			self.db_cursor.execute(query)
			rs = self.db_cursor.fetchone()
			if rs:
				fail_result, =rs

			new_query = "select count(message_type) from reporting_taskdetail where task_id_id=%s and message_type='ERROR'" % task_id
			self.db_cursor.execute(new_query)
			rs = self.db_cursor.fetchone()
			if rs:
				error_result, =rs

			if fail_result == 0 and error_result == 0:
				bpassed = True
			else:
				bpassed = False
		except Exception,e:
			print "Error happend when query task test result", str(e)
		finally:
			self.disconnect()
		return bpassed, fail_result, error_result

	def delete_configs_table(self):
		try:
			delete_details = "delete from configs_configdetails"
			self.db_cursor.execute(delete_details)
			self.db_conn.commit()
			
			delete_summary = "delete from configs_configsummary"
			self.db_cursor.execute(delete_summary)
			self.db_conn.commit()	
		except Exception,e:
			print "Exception happend when insert config summary. " + str(e)
		finally:
			self.disconnect()

	def insert_config_summary(self, project, test_type, configs):
		#{'javaagent': 
		#	{'regression': ['1', '2', '3', '4', '5', '6'], 
		#	'bvt': ['1']  }}
		config_id = -1
		try:
			insert = "insert into configs_configsummary (project, test_type, configs) values ('%s', '%s', '%s')" % (project, test_type, configs)
			self.db_cursor.execute(insert)
			self.db_conn.commit()
			query = "select csid from configs_configsummary where test_type = '%s' and project = '%s'" % (test_type, project)
			self.db_cursor.execute(query)
			rs = self.db_cursor.fetchone()
			if rs:
				config_id, = rs

		except Exception,e:
			print "Exception happend when insert config summary. " + str(e)
		finally:
			self.disconnect()
		return config_id			

	def insert_config_detail(self, csid, config_id, config):
		if config['server']:
			test_type = 'TPS Server'
			jdk = 'no'
			demo = 'no'
			middleware = 'no'
		elif config['agent']:
			test_type = 'Java Agent'
			for file_path in config['files']:
				file_name = file_path.split('/')[-1]
				if 'jdk' in file_name:
					jdk = file_name
				elif 'tomcat' in file_name:
					middleware = file_name
				elif '.war' in file_name:
					demo = file_name

		links_list = []
		if config['link']:
			for link in config['link']:
				links_list.append("Link to container with name %s using its alias %s." % (link['container_name'], link['alias']))
				links = '<br>'.join(links_list)
		else:
			links = 'No link for this container.'

		ports_list = []
		if config['ports']:
			for port in config['ports']:
				ports_list.append("Container is using port %s mapping to host %s using port with %s." % (port['container'], HOST, port['map']))
			ports = '<br>'.join(ports_list)	
		else:
			ports = "No port used for mapping."

		try:
			insert = '''
			insert into configs_configdetails (csid_id, config_id, config_type, container_name, 
			container_alias, image_name, image_path, links, ports, demo, jdk, middleware, config_desc)
			values (%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' )
			''' % (csid, config_id, test_type, config['container_name'], config['container_alias'], config['image_name'], 
				config['tar_path'], links, ports, demo, jdk, middleware, config['description']
				)
			self.db_cursor.execute(insert)
			self.db_conn.commit()

		except Exception,e:
			print "Exception happend when insert config details. " + str(e)
		finally:
			self.disconnect()

	def get_scheduled_task(self, test_status):
		result = []
		try:
			query = "select min(sid) from reporting_summary where test_status='%s'" % test_status
			self.db_cursor.execute(query)
			rs = self.db_cursor.fetchone()

			if rs:
				sid, = rs

			if sid:
				new_query = "select * from reporting_summary where sid = '%s'" % sid
				self.db_cursor.execute(new_query)
				rs = self.db_cursor.fetchone()
				if rs:
					for item in rs:
						result.append(item)

		except Exception,e:
			print "Error happend when query task test result", str(e)
		finally:
			self.disconnect()

		return result

	def update_test_case_result(self, task_id, result):
		updated_time = time.strftime(GLOBAL_TIME_FORMAT, time.localtime())
		try:
			query = "update reporting_tasks set test_result='%s', task_updated='%s' where task_id=%s" % (result, updated_time, task_id)
			self.db_cursor.execute(query)
			self.db_conn.commit()

		except Exception,e:
			print "Exception happend when updating test case result" + str(e)
		finally:
			self.disconnect()

	def delete_multiple_config_record(self, sid):
		try:
			query = "delete from reporting_summary where sid='%s'" % sid
			self.db_cursor.execute(query)
			self.db_conn.commit()

		except Exception,e:
			print "Exception happend when updating test case result" + str(e)
		finally:
			self.disconnect()

	def get_task_test_result(self, sid):
		bpassed = False
		try:
			query = "select count(test_result) from reporting_tasks where sid_id=%s and test_result='FAIL'" % sid
			self.db_cursor.execute(query)
			rs = self.db_cursor.fetchone()
			if rs:
				fail_result, =rs

			new_query = "select count(test_result) from reporting_tasks where sid_id=%s and test_result='PASS'" % sid
			self.db_cursor.execute(new_query)
			rs = self.db_cursor.fetchone()
			if rs:
				pass_result, =rs

			if fail_result ==0:
				bpassed = True
			else:
				bpassed = False
		except Exception,e:
			print "Error happend when query task test result", str(e)
		finally:
			self.disconnect()
		return bpassed, fail_result, pass_result

	def get_test_status_by_sid(self, sid):
		result = ''
		try:
			query = "select test_status from reporting_summary where sid=%s" % str(sid)
			self.db_cursor.execute(query)
			rs = self.db_cursor.fetchone()
			if rs:
				result, =rs
		except Exception,e:
			print "Error happend when query test status by sid", str(e)
		finally:
			self.disconnect()
		return result

	def get_configs_using_fixed_value(self, fixed_value):
		# output result like [222L, 223L, 224L] ['1', '2', '3']
		sid_list = []
		config_list = []
		created_list = []
		updated_list = []
		try:
			query = "select sid, config_id, created, updated from reporting_summary where summary_desc like '%{0}%'".format(fixed_value)
			self.db_cursor.execute(query)
			rs = self.db_cursor.fetchall()
			if rs:
				for item in rs:
					sid, config_id, created_time, updated_time = item
					sid_list.append(sid)
					config_list.append(config_id)
					created_list.append(created_time)
					updated_list.append(updated_time)

		except Exception,e:
			print "Error happend when query task test result", str(e)
		finally:
			self.disconnect()
		return sid_list, config_list, created_list, updated_list

	def get_bvt_task_end_time(self, sid):
		try:
			query = "select updated from reporting_summary where sid='%s'" % sid
			self.db_cursor.execute(query)
			rs = self.db_cursor.fetchone()
			if rs:
				result, = rs

		except Exception,e:
			print "Error happend when query task test result", str(e)

		finally:
			self.disconnect()
		return result

	def output_test_case_log(self, task_id, msg_type, msg_content, attachment):
		if task_id == -1:
			return
		try:
			query = "insert into reporting_taskdetail (message_type, message_content, task_id_id, file_path)  values ('%s', '%s', %s, '%s')" % (msg_type, msg_content, task_id, attachment)
			self.db_cursor.execute(query)
			self.db_conn.commit()

		except Exception,e:
			print "Exception happend when output test case logs. " + str(e)
		finally:
			self.disconnect()

	def initiallize_test_case(self, sid, task_name, task_desc):
		result = 0
		current_time = time.strftime(GLOBAL_TIME_FORMAT, time.localtime())
		try:
			query = "insert into reporting_tasks (sid_id, task_name, task_desc, task_created, test_result, task_updated) values (%s, '%s', '%s', '%s', '%s', '%s')" % (sid, task_name, task_desc, current_time, 'unkown', current_time)
			self.db_cursor.execute(query)
			self.db_conn.commit()

			new_query = "select task_id from reporting_tasks where sid_id = %s and task_name='%s' " % (sid, task_name)
			self.db_cursor.execute(new_query)
			rs = self.db_cursor.fetchone()
			if rs:
				result, = rs
		except Exception,e:
			print 'Exception happend when initializing test cases.', str(e)

		finally:
			self.disconnect()
		return result

class NewTestRun(object):
	def get_query(self, **kwargs):
		query_type = "insert"
		start_time = time.strftime(GLOBAL_TIME_FORMAT, time.localtime())
		query = "INSERT INTO reporting_summary (test_type, config_id, test_status, proj_name, user_name, build_info, summary_desc, created, updated) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (kwargs['test_type'], kwargs['config_id'], kwargs['test_status'], kwargs['proj_name'], kwargs['user_name'], kwargs['build_info'], kwargs['summary_desc'], start_time, start_time)
		return query_type, query

class SelectMaxId(object):
	def get_query(self, **kwargs):
		query_type = "selectone"
		query = "select max(sid) from reporting_summary"
		return query_type, query

class UpdateTestRunStatus(object):
	def get_query(self, **kwargs):
		query_type = "insert"
		updated_time = time.strftime(GLOBAL_TIME_FORMAT, time.localtime())
		query = "UPDATE reporting_summary SET test_status='%s', updated='%s' where sid=%s" %(kwargs['status'], updated_time, kwargs['sid'])
		return query_type, query

class GetResultByStatus(object):
	def get_query(self, **kwargs):
		query_type = "selectlist"
		query = "select * from reporting_summary where test_status='%s'" % kwargs['status']
		return query_type, query

if __name__=="__main__":
	result = OperateMySQL().get_test_status_by_sid(1)
	if result:
		print result
	else:
		print 'no value', result

