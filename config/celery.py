import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODUL", 'config.settings')

app = Celery('SoundSphere')
app.config_from_object('django.conf.settings', namespace='CELERY')
app.autodiscover_tasks()