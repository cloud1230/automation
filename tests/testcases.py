###########################################################
# Below TESTCASES and REG_TESTCASES are examples for 
# email_report.py, it will be sent in the email report.
#
###########################################################

TESTCASES= [
	{'name':'001_Connect To Server', 'priority':'1-High', 'goal':'Verify java agent could connect to tps server successfully.'},
	{'name':'002_No Severe Log', 'priority':'1-High', 'goal':'Verify java agent log has no exceptions.'},
	{'name':'003_APP Name', 'priority':'1-High', 'goal':'Verify app name in java agent property file display correct in server.'},
	{'name':'004_Tier Name', 'priority':'1-High', 'goal':'Verify tier name in java agent property file display correct in server.'},
	{'name':'005_Demo Program Works', 'priority':'1-High', 'goal':'Verify demo program works while installing java agent.'},
	{'name':'006-Topo Works', 'priority':'1-High', 'goal':'Verify topo display as expected in tps server.'},
	{'name':'007_Slow SQL', 'priority':'1-High', 'goal':'Verify enable slow sql in java agent property file would work well in tps server.'},
	{'name':'008_Slow Trace', 'priority':'1-High', 'goal':'Verify slow trace could be captured'},
	{'name':'009_Slow Web Transaction', 'priority':'1-High', 'goal':'Verify enable slow transaction in java agent property file would work well in tps server.'},
	{'name':'010_Background Task Works', 'priority':'1-High', 'goal':'Verify Background task could be captured by java agent and display well in tps server.'},
	{'name':'011_Using default properties file', 'priority':'1-High', 'goal':'Verify java agent use its default properties files.'},
	]

REG_TESTCASES= [
	{'name':'001_Connect To Server', 'priority':'1-High', 'goal':'Verify java agent could connect to tps server successfully.'},
	{'name':'002_No Severe Log', 'priority':'1-High', 'goal':'Verify java agent log has no exceptions.'},
	{'name':'003_APP Name', 'priority':'1-High', 'goal':'Verify app name in java agent property file display correct in server.'},
	{'name':'004_Tier Name', 'priority':'1-High', 'goal':'Verify tier name in java agent property file display correct in server.'},
	{'name':'005_Demo Program Works', 'priority':'1-High', 'goal':'Verify demo program works while installing java agent.'},
	{'name':'006-Topo Works', 'priority':'1-High', 'goal':'Verify topo display as expected in tps server.'},
	{'name':'007_Slow SQL', 'priority':'1-High', 'goal':'Verify enable slow sql in java agent property file would work well in tps server.'},
	{'name':'008_Slow Trace', 'priority':'1-High', 'goal':'Verify slow trace could be captured'},
	{'name':'009_Slow Web Transaction', 'priority':'1-High', 'goal':'Verify enable slow transaction in java agent property file would work well in tps server.'},
	{'name':'010_Background Task Works', 'priority':'1-High', 'goal':'Verify Background task could be captured by java agent and display well in tps server.'},
	{'name':'011_Using default properties file', 'priority':'1-High', 'goal':'Verify java agent use its default properties files.'},
	{'name':'012_Insert Browser Code using text Works', 'priority':'1-High', 'goal':'Verify java agent could insert jsp code to your web demo pages.'},	
	{'name':'013_Memcached Java client 2.0.1 Works', 'priority':'2-Medium', 'goal':'Verify using memcached java client 2.0.1 could get correct display in tps server.'},		
	{'name':'014_Jedis 2.6 Works', 'priority':'2-Medium', 'goal':'Verify using jedis 2.6 could get correct display in tps server.'},		
	{'name':'015_MongoDB 3 Works', 'priority':'2-Medium', 'goal':'Verify using mongodb3 could get correct display in tps server.'},		
	{'name':'016_MySQL Java client Works', 'priority':'2-Medium', 'goal':'Verify using mysql java client could get correct display in tps server.'},			
	{'name':'017_Check open file numbers', 'priority':'2-Medium', 'goal':'Verify using java agent would not cause opening too many files.'},			
	{'name':'018_AI supports BI using cookie', 'priority':'1-High', 'goal':'Verify using java agent would support BI using cookie parameters ONEAPM_AI.'},			
	{'name':'019_AI supports BI using header', 'priority':'1-High', 'goal':'Verify using java agent would support BI using header parameter ONEAPM_AI.'},
	{'name':'020_Check JVM memory data', 'priority':'1-High', 'goal':'Verify using java agent would send correct memory data to tps server.'},
	{'name':'021_Check JVM thread data', 'priority':'1-High', 'goal':'Verify using java agent would send correct thread data to tps server.'},
	{'name':'022_Check JVM session data', 'priority':'1-High', 'goal':'Verify using java agent would send correct session data to tps server.'},	
	{'name':'023_Check unable to load interface problem', 'priority':'2-Medium', 'goal':'Verify there is no unable to load interface problem in java agent log.'},	
	]

TESTCASES_TYPES = {
	'bvt': TESTCASES,
	'regression': REG_TESTCASES,
}