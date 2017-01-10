import os

def generate_temp_log():
	logName="templog"+time.strftime("%Y%m%d%H%M%S")+".log"
	logPath=os.path.join(BASE_DIR, 'logs', logName)

	if os.path.isfile(logPath):
		os.system("rm -rf {0}".format(logPath))

	os.system("touch {0}".format(logPath))
	os.system("chmod 777 {0}".format(logPath))

	time.sleep(2)
	return logPath

def clean_for_spaces():
	os.system("rm -rf /tmp/*")


