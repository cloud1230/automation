#  Quick Start for Web Automation Testing

### Introduction
This is the Web UI testing framework aimed for the UI automation testing with selenium for testing team. This framework will finish the base function of logging, snapshot, test cases organization, test data parsing, email and result showing.

### Prerequisite
* Create a database with name webautomation
* Run command pip install -r requirements.txt 


### Steps to configure
* create db first time
** python manage.py makemigrations
** python manage.py migrate
* create superuser
** python manage.py createsuperuser
* start server
** python manage.py runserver ip:port
* navigate to screenshot folder, start web service
** python -m SimpleHTTPServer 22222 &
