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

### How to start web automation testing？
* Run command StartTest.py
<code>
Example: ./StartTest --run_type bvt --project AI --user_email zhangziyi@oneapm.com 	--browser firefox --build_info 4.1.1.0 --description 'This is a test run.' --start
</code>

<code>-h   --help     Will show help information.</code>
<code>-s   --start    Will create a test run for your automation test.</code>
<code>--run_type      Need to pass run type parameter.</code>
<code>--project       Need to set project parameter.</code>
<code>--user_email    Need to set user email parameter.</code>
<code>--browser       Need to set browser parameter.</code>
<code>--build_info    Need to set build infor parameter.</code>
<code>--description   Need to set test description parameter.</code>
