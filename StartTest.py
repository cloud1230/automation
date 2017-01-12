#!/usr/bin/env python
import os
import sys
import getopt
from common.database_wrapper import *
from common.constants import *

class TestRunParams(UserDict):
	def __init__(self):
		UserDict.__init__(self)
		self['run_type'] = 'bvt'
		self['project'] = 'ai'
		self['user_email'] = 'zhangziyi@oneapm.com'
		self['browser'] = 'firefox'
		self['build_info'] = '4.1.1.0'
		self['description'] = 'This is a test.'

		self.oneapm_email()
		self.format_output()

	def oneapm_email(self):
		if not "@oneapm.com" in self['user_email']:
			print "ERROR: You are using invalid email. You should enter oneapm email address."
			sys.exit(-1)

	def format_output(self):
		print "You entered parameters are as follows:\n" + \
			"Run type:".ljust(20) + self['run_type'] + "\n" + \
			"Project:".ljust(20) + self['project'] + "\n" + \
			"User email:".ljust(20) + self['user_email'] + "\n" + \
			"Browser:".ljust(20) + self['browser'] + "\n" + \
			"Build info:".ljust(20) + self['build_info'] + "\n" + \
			"Description:".ljust(20) + self['description'] + "\n"

def start(run_type, project, user_email, browser, build_info, description):
	new_test_run = OperateMySQL(NewTestRun)
	new_test_run.operate_query(
		test_type = run_type, 
		test_status = TASK_STATUS['Sch'], 
		proj_name = project, 
		user_email = user_email, 
		browser = browser,
		build_info = build_info,
		summary_desc = description, 
		)

def usage():
	print "Start web automation test run using command......"
	print "Example: ./StartTest --run_type bvt --project AI --user_email zhangziyi@oneapm.com \
	--browser firefox --build_info 4.1.1.0 --description \'This is a test run.\' --start"
	print "-h   --help     Will show help information."
	print "-s   --start    Will create a test run for your automation test."
	print ""
	sys.exit(0)

def main():
	test_run_params = TestRunParams()

	if not len(sys.argv[1:]):
		usage()
	try:
		opts, args = getopt.getopt(sys.argv[1:], 
        				"sh", 
        				[
			        	"start", 
			        	"help", 
			        	"run_type=",
			        	"project=",
			        	"user_email=",
			        	"browser=",
			        	"build_info=",
			        	"description="
			        	])

	except getopt.GetoptError as err:
		print err
		usage()

	for o,a in opts:
		if o in ("-h", "--help"):
			usage()

		if o in ("-s", "--start"):
			start(test_run_params['run_type'],
				test_run_params['project'],
				test_run_params['user_email'],
				test_run_params['browser'],
				test_run_params['build_info'],
				test_run_params['description']
				 )

		if o in ("--run_type"):
			test_run_params['run_type'] = a.strip()

		if o in ("--project"):
			test_run_params['project'] = a.strip()

		if o in ("--user_email"):
			test_run_params['user_email'] = a.strip()

		if o in ("--browser"):
			test_run_params['browser'] = a.strip()

		if o in ("--build_info"):
			test_run_params['build_info'] = a.strip()

		if o in ("--description"):
			test_run_params['description'] = a.strip()

if __name__=='__main__':
	main()