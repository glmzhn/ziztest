from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Task, Notification, User


@admin.register(Task)
class TaskAdmin(ModelAdmin):
    list_display = ['title', 'status', 'user', 'due_date']
    list_filter = ['status', 'user']


@admin.register(Notification)
class NotificationAdmin(ModelAdmin):
    list_display = ['task', 'message', 'created_at']


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ['username', 'email', 'is_active']
