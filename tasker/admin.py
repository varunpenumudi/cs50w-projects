from django.contrib import admin
from .models import User, Task, SubTask


class TaskAdmin(admin.ModelAdmin):
    list_display = ("task_name","description","updated")

class SubTaskAdmin(admin.ModelAdmin):
    list_display = ("subtask_name","parent_task", "completed")

# Register your models here.
admin.site.register(User)
admin.site.register(Task, TaskAdmin)
admin.site.register(SubTask, SubTaskAdmin)