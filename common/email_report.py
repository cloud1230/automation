# -*- coding: utf-8 -*-  

from UserDict import UserDict
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import password
import constants
import sys
sys.path.append('..')
import tests.testcases

class EmailReportBuilder(UserDict):
	def __init__(self, builds=None):
		UserDict.__init__(self)
		# builds = "server_version: xxx;project:xxx"
		self['server_version'] = ''
		self['project'] = ''

		if builds is not None:
			lbuilds = builds.split(";")
			for build in lbuilds:
				sName, sNum = build.split(":")
				self[sName] = sNum

	def get_test_case_list(self, case_type):
		return tests.testcases.TESTCASES_TYPES.get(case_type)

	def get_html_header(self):
		return '''
        <html><head>
        <style>   
        <!--
         /* Font Definitions */
         @font-face
        {font-family:Calibri;panose-1:2 1 6 0 3 1 1 1 1 1; mso-font-alt:Calibri;
            mso-font-charset:134;
            mso-generic-font-family:auto;
            mso-font-pitch:variable;
            mso-font-signature:3 680460288 22 0 262145 0;}         
        /* Style Definitions */
        p.MsoNormal, li.MsoNormal, div.MsoNormal {mso-style-unhide:no;mso-style-qformat:yes;mso-style-parent:"";margin:0in; margin-bottom:.0001pt; mso-pagination:widow-orphan;font-size:12.0pt;}
        a:link, span.MsoHyperlink {mso-style-noshow:yes;mso-style-priority:99;color:blue;text-decoration:underline;text-underline:single;}
        a:visited, span.MsoHyperlinkFollowed {mso-style-noshow:yes;mso-style-priority:99;color:purple;text-decoration:underline;text-underline:single;}
        p {mso-style-noshow:yes;mso-style-priority:99;mso-margin-top-alt:auto;margin-right:0in; mso-margin-bottom-alt:auto; margin-left:0in;mso-pagination:widow-orphan;font-size:12.0pt;}
        table {border-width: 1px;border-spacing: 0px;border-style: solid;border-color: gray;border-collapse: collapse;background-color: white;font-size:10.0pt;}
        tr            {mso-yfti-irow:1;height:12pt;font-size:10.0pt;color:black}
        tr.data       {mso-yfti-irow:1;height:12pt;font-size:10.0pt;color:black}
        tr.datafail   {mso-yfti-irow:1;height:12pt;font-size:10.0pt;color:red}
        tr.dataheader {mso-yfti-irow:0;mso-yfti-firstrow:yes;height:12pt;background:yellow;font-size:10.0pt;color:black}
        -->
        </style>
        </head>'''

	def get_body_top_html_text(self):
		return '''
  		<body>
        <p><b><span>Builds used in test:</span></b><br>'''

	def get_build_info_html_text(self):
		build_info_text = '''<table>
        <tr><td><b>Project: </b></td><td>%s</td></tr>
        <tr><td><b>Server Version: </b></td><td>%s/td></tr>
        </table></br></br>'''

		return build_info_text % (self['project'], self['server_version'])

	def get_bvt_header_row_HTML_text (self):
		return '''
		<b><span>Test Log:</span></b>
		<table border="1">
		<tr class=dataheader>
		<td>SID</td><td>Product</td><td>Config ID</td>
		<td>Test Type</td><td>Pass</td><td>Fail</td><td>Total</td>
		<td>PassPercent</td><td>Start Time</td><td>End Time</td>
		</tr>'''

	def get_bvt_test_run_data_row_HTML_text (self, dataRow, bPASSED):
		if bPASSED:sTableClass = "data"
		else: sTableClass = "datafail"

		#dataRow = row_content.split(',')
		return ('''
		<tr class=%s>
		<td><a href="%s/%s">%s</a></td><td>%s</td><td>%s</td><td>%s</td>
		<td>%s</td>
		<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>
		</tr>''') % (sTableClass, constants.SERVER_ADDRESS, dataRow[0], dataRow[0], 
		dataRow[1],dataRow[2],dataRow[3], dataRow[4], #Log result Link
		dataRow[5],dataRow[6],dataRow[7],dataRow[8], dataRow[9])

	def get_regression_test_run_data_row_HTML_text(self, rows, bpassed_list):
		row_content = ''
		for i in range(len(bpassed_list)):
			if bpassed_list[i]:
				sTableClass = "data"
			else:
				sTableClass = "datafail"

			row_content += ('''
				<tr class=%s>
				<td><a href="%s/%s">%s</a></td><td>%s</td><td>%s</td><td>%s</td>
				<td>%s</td>
				<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>
				</tr>''') % (sTableClass, constants.SERVER_ADDRESS, rows[i][0], rows[i][0], rows[i][1],
				rows[i][2], rows[i][3], rows[i][4], #Log result Link
				rows[i][5], rows[i][6], rows[i][7], rows[i][8], rows[i][9])

		return row_content

	def get_body_bottom_html_text(self):
		return '''</table></body></html>'''

	def get_test_case_info_html_text(self, case_type):
		sHTML = '''
		<span><b>Test cases:</b></span>
		<table>
		<tr class=dataheader><td><p><span>Test Name</span></p></td>
		<td><p><span>Priority</span></p></td>
		<td><p><span>Test Objective</span></p></td></tr>
		'''
		testcases = self.get_test_case_list(case_type)
		if testcases:
			for testcase in testcases:
				sHTML += '''
					<tr>
					<td><p><span>%s</span></p></td>
					<td><p><span>%s</span></p></td>
					<td><p><span>%s</span></p></td>
					</tr>  ''' % (testcase['name'], testcase['priority'], testcase['goal'])

		sHTML += '</table></br></br>'
		return sHTML

	def get_bvt_email_html_text(self, row_content, bPASSED):
		content = self.get_html_header()

		content += self.get_body_top_html_text()
		content += self.get_build_info_html_text()
		content += self.get_test_case_info_html_text('bvt')
		content += self.get_bvt_header_row_HTML_text()
		content += self.get_bvt_test_run_data_row_HTML_text(row_content, bPASSED)
		content += self.get_body_bottom_html_text()

		return content

	def get_regression_email_html_text(self, rows, bpassed_list):
		content = self.get_html_header()

		content += self.get_body_top_html_text()
		content += self.get_build_info_html_text()
		content += self.get_test_case_info_html_text('regression')
		content += self.get_bvt_header_row_HTML_text()
		content += self.get_regression_test_run_data_row_HTML_text(rows, bpassed_list)
		content += self.get_body_bottom_html_text()

		return content

	def send_report(self, sub, msg, to=[constants.EMAIL_SENDER], cc=[]):
		mail_server = constants.EMAIL_SERVER
		mail_user = constants.EMAIL_SENDER
		mail_pass = password.email_pass

		from_mail = constants.EMAIL_SENDER

		html_text = msg

		msg_root = MIMEMultipart('related')
		msg_root['Subject'] = sub
		msg_root['From'] = from_mail
		msg_root['To'] = ';'.join(to)
		msg_root['cc'] = ';'.join(cc)

		msg_alternative = MIMEMultipart('alternative')
		msg_root.attach(msg_alternative)
		msg_html = MIMEText(html_text, 'html', 'utf-8')
		msg_alternative.attach(msg_html)

		try:
			s = smtplib.SMTP_SSL()
			s.connect(mail_server, port=constants.EMAIL_PORT)

			s.login(mail_user, mail_pass)

			s.sendmail(from_mail, to, msg_root.as_string())
			s.quit()
			print '.............Email report sent out %s ' % sub

		except Exception,e:
			print 'Exception in sending the email report, exception: \n', str(e)
	

if __name__=='__main__':
	pass
	#bvt_mail = EmailReportBuilder(':')
	#bvt_mail.send_report('Performance result', '', to=['zhangziyi@oneapm.com'])

