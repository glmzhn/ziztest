import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zhtest.settings')

app = Celery('zhtest')
app.config_from_object('django.conf:settings')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from zhtest.tasks import check_overdue_tasks
    sender.add_periodic_task(600.0, check_overdue_tasks.s(), name='check overdue myapp every 10 minutes')
