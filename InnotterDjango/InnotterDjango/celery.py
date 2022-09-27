from celery import Celery
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InnotterDjango.settings')

app = Celery('InnotterDjango')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
