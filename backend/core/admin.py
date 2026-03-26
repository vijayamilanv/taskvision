from django.contrib import admin  # pyre-ignore
from .models import Project, Task, TaskComment, TaskActivity, Notification  # pyre-ignore

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'priority', 'assigned_to', 'owner', 'created_at')
    list_filter = ('status', 'priority', 'assigned_to')
    search_fields = ('name', 'description')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'deadline', 'assigned_to', 'created_at')
    list_filter = ('status', 'priority', 'assigned_to', 'project')
    search_fields = ('title', 'description')

@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'created_at')
    list_filter = ('user',)

@admin.register(TaskActivity)
class TaskActivityAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'activity_type', 'created_at')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'is_read', 'created_at')
    list_filter = ('is_read', 'user')
