import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formulario_captura.settings')

app = Celery('formulario_captura')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
