#  Quick Start for Web Automation Testing

### Introduction
This is the Web UI testing framework aimed for the UI automation testing with selenium for testing team. This framework will finish the base function of logging, snapshot, test cases organization, test data parsing, email and result showing.

### Prerequisite
* Create a database with name webautomation
* Run command pip install -r requirements.txt 


### Steps to configure
* create db first time

```shell
	python manage.py makemigrations
	python manage.py migrate
```

* create superuser

```shell
	python manage.py createsuperuser
```

* start server

```shell
	python manage.py runserver ip:port
```

* navigate to screenshot folder, start web service

```shell
	python -m SimpleHTTPServer 22222 &
```	

### How to start web automation testing？

* Run command StartTest.py

```shell
	Example: ./StartTest --run_type bvt --project AI --user_email zhangziyi@oneapm.com 	--browser firefox --build_info 4.1.1.0 --description 'This is a test run.' --start

	-h   --help     Will show help information.
	-s   --start    Will create a test run for your automation test.
    --run_type      Need to pass run type parameter.
    --project       Need to set project parameter.
    --user_email    Need to set user email parameter.
    --browser       Need to set browser parameter.
    --build_info    Need to set build infor parameter.
    --description   Need to set test description parameter.
```

### How to write new web automation test cases？

* Create module XXXTestCases.py under tests/webtest .

* Create class XXXTestRun in XXXTestCases.py inherited class BaseTestRun from module BaseTestCases.

```shell
from BaseTestCases import *

class BVTTestRun(BaseTestRun):
	pass
```

* In XXXTestRun rewrite method running_test_case_list and add defined test cases under this method.

```shell
class BVTTestRun(BaseTestRun):
	def running_test_case_list(self):
		self.test_login()
		pass
```

* Above your own defined test cases add decorators with test case name and description

```shell
@testcase('003_TestLogin', 'Verify we can correctly login tps server.')
	def test_login(self):
```

* In each test cases you need to add try catch of your steps

```shell
try:
	if self.force_stop:
			raise SkipTestException("Exiting text case %s for critical issues......" % self.testname)

	#test cases steps here
	pass

except SkipTestException, e:
	self.force_stop = True
	getLog().Error(e.error)

except Exception, e:
	self.force_stop = True
	getLog().Error(self.testname+': '+ str(e))
```
* Then register your newly added test cases with a defined test type in TestEngine.py

```shell
from tests.webtest.BVTTestCases import *
def run_ai_scheduled_task(self, task, scen_logger):
	if task[1] == 'bvt':
		print 'Running java agent bvt related tasks...'
		BVTTestRun(scen_logger).run()
```