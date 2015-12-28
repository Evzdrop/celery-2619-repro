from __future__ import absolute_import

import os

from celery import Celery
from django.conf import settings

import time
import sys

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'repro.settings')

app = Celery('repro')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')

from celery.signals import task_failure  

def process_failure_signal(exception, traceback, sender, task_id, args, kwargs, einfo, **kw):
    print exception
    print traceback

task_failure.connect(process_failure_signal)  

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

