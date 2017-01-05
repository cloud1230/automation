This is the Web UI testing framework aimed for the UI automation testing with selenium for testing team. This framework will finish the base function of logging, snapshot, test cases organization, test data parsing, email and result showing.

Prerequisite:
1. Create a database with name webautomation
2. Run command pip install -r requirements.txt 


Steps:
1.create db first time
python manage.py makemigrations
python manage.py migrate
2.create superuser
python manage.py createsuperuser
3.start server
python manage.py runserver \<ip\>:\<port\>
4.navigate to screenshot folder, start web service
python -m SimpleHTTPServer 22222 &

