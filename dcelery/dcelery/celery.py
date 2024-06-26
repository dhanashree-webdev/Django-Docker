import os 
from celery import Celery

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dcelery.settings')
app = Celery("dcelery")
app.config_from_object('django.conf:settings', namespace='CELERY')

@app.task
def divide(x, y):
    import time
    time.sleep(5)
    return x / y

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
