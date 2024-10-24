from celery import shared_task
from django.utils import timezone


@shared_task
def send_task_notification(task_id):
    from myapp.models import Task, Notification
    task = Task.objects.get(id=task_id)
    Notification.objects.create(task=task, message=f'Task "{task.title}" is overdue!')


@shared_task
def check_overdue_tasks():
    from myapp.models import Task
    overdue_tasks = Task.objects.filter(status='pending', due_date__lt=timezone.now())
    for task in overdue_tasks:
        send_task_notification.delay(task.id)
