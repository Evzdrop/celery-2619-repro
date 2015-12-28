from celery import shared_task
import requests, json, ast

from django.conf import settings
from repro.monitoring.custom_metrics import custom_metric_timed_node, record_metric

from math import ceil, floor

import logging
logger = logging.getLogger(__name__)

@shared_task()
@custom_metric_timed_node("Custom/index_object/1")
def index_object(model, post=None, index=None, person=None, ttl=None, refresh=False):
    requests.get('https://yahoo.com') # Fake IO request
