from celery.schedules import crontab
from celery import Celery
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InnotterDjango.settings')

app = Celery('InnotterDjango')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'add-every-midnight':
    {
        'task': 'InnotterDjango.tasks.clear_database_from_waste_accounts',
        'schedule': crontab(minute=0, hour=0),
    },
}

app.autodiscover_tasks()
