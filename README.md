#  Quick Start for Web Automation Testing

### Introduction
This is the Web UI testing framework aimed for the UI automation testing with selenium for testing team. This framework will finish the base function of logging, snapshot, test cases organization, test data parsing, email and result showing.

### Prerequisite
* Create a database with name webautomation
* Run command pip install -r requirements.txt 


### Steps to configure
* create db first time
	python manage.py makemigrations
	python manage.py migrate
* create superuser
	python manage.py createsuperuser
* start server
	python manage.py runserver ip:port
* navigate to screenshot folder, start web service
	python -m SimpleHTTPServer 22222 &

### How to start web automation testing？
* Run command StartTest.py

	Example: ./StartTest --run_type bvt --project AI --user_email zhangziyi@oneapm.com 	--browser firefox --build_info 4.1.1.0 --description 'This is a test run.' --start

	-h   --help     Will show help information.
	-s   --start    Will create a test run for your automation test.
    --run_type      Need to pass run type parameter.
    --project       Need to set project parameter.
    --user_email    Need to set user email parameter.
    --browser       Need to set browser parameter.
    --build_info    Need to set build infor parameter.
    --description   Need to set test description parameter.
