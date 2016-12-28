import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = '10.128.9.180'
LOG_PORT = 22222
SNAPSHOT_FOLDER = os.path.join(BASE_DIR, 'screenshot')
GLOBAL_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_DB_SERVER = '10.128.9.180'
LOG_DB_USER = 'root'
LOG_DB_PASS = 'mysql'
LOG_DATABASE = 'webautomation'
LOG_DB_PORT = 3306
SERVER_ADDRESS = "http://%s/reporting" % HOST
EMAIL_SERVER = 'smtp.exmail.qq.com'
EMAIL_PORT = 465
EMAIL_SENDER = 'zhangziyi@oneapm.com'
EMAIL_TO_LIST = [
	'zhangziyi@oneapm.com', 
	]
TASK_STATUS = {
		'Debug': 'Debugging',
		'Cal': 'Canceled',
		'Run': 'Running',
		'Fin': 'Finished',
		'Sch': 'Scheduled',
	}
