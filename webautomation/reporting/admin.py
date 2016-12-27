from django.contrib import admin
from .models import Summary, Tasks, TaskDetail
# Register your models here.
class SummaryAdmin(admin.ModelAdmin):
	list_display = ["sid", "browser","test_type", "test_status", "proj_name", "user_email", "build_info", "summary_desc", "created", "updated"]

class TaskDetailAdmin(admin.ModelAdmin):
	list_display = ["message_type", "message_content", "file_path", "task_id"]

admin.site.register(Summary, SummaryAdmin)
admin.site.register(Tasks)
admin.site.register(TaskDetail, TaskDetailAdmin)