from celery import shared_task
from django.utils import timezone


@shared_task
def send_task_notification(task_id):
    from myapp.models import Task, Notification
    task = Task.objects.get(id=task_id)
    Notification.objects.create(task=task, message=f'Task "{task.title}" is overdue!')


@shared_task
def check_overdue_tasks():
    from myapp.models import Task, Notification
    overdue_tasks = Task.objects.filter(due_date__lt=timezone.now()).exclude(status='overdue')
    for task in overdue_tasks:
        task.status = 'overdue'
        task.save()

        if not Notification.objects.filter(task=task).exists():
            Notification.objects.create(
                task=task,
                message=f"Задача {task.title} просрочена."
            )
