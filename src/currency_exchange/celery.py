import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'currency_exchange.settings')

os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

app = Celery('currency_exchange')


app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
