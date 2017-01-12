#  Quick Start for Web Automation Testing

### Introduction
This is the Web UI testing framework aimed for the UI automation testing with selenium for testing team. This framework will finish the base function of logging, snapshot, test cases organization, test data parsing, email and result showing.

### Prerequisite
* Create a database with name webautomation
* Run command pip install -r requirements.txt 


### Steps to configure
* create db first time
<pre><code>
 python manage.py makemigrations
 python manage.py migrate
</code></pre>
* create superuser
<pre><code>
 python manage.py createsuperuser
</code></pre>
* start server
<pre><code>
 python manage.py runserver ip:port
</code></pre>
* navigate to screenshot folder, start web service
<pre><code>
 python -m SimpleHTTPServer 22222 &
</code></pre>

### How to write test cases？
* 