from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Summary(models.Model):
	class Meta:
		ordering = ["-sid",]
		
	sid = models.AutoField(primary_key=True)
	test_type = models.CharField(max_length=50)
	test_status = models.CharField(max_length=50)
	proj_name = models.CharField(max_length=50)
	user_email = models.EmailField()
	browser = models.CharField(max_length=50)
	build_info = models.CharField(max_length=200)
	summary_desc = models.TextField()
	created = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return str(self.sid)

class Tasks(models.Model):
	task_id = models.AutoField(primary_key=True)
	sid = models.ForeignKey(Summary, on_delete=models.CASCADE)
	task_name = models.CharField(max_length=200)
	task_desc = models.TextField()
	test_result = models.CharField(max_length=50,blank=True,null=True)
	task_created = models.DateTimeField(auto_now_add=True, auto_now=False)
	task_updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return self.task_name

class TaskDetail(models.Model):
	task_id = models.ForeignKey(Tasks, on_delete=models.CASCADE)
	message_type = models.CharField(max_length=50)
	message_content = models.TextField()
	file_path = models.CharField(max_length=200, null=True, blank=True)

	def __unicode__(self):
		return self.message_content