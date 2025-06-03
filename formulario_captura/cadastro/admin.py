from django.contrib import admin
from .models import Cliente
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule

admin.site.register(Cliente)
