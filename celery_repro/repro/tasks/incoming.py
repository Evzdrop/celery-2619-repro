import json
import requests
from celery import shared_task
from repro.monitoring.custom_metrics import custom_metric_timed_node

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

@shared_task()
@custom_metric_timed_node('Custom/incoming/twitter/2')
def incoming(tweet, *args, **kwargs):
    parsed = json.loads(tweet)

    return parsed

@custom_metric_timed_node('Custom/incoming/infer_location/3')
def infer_location(post):
    requests.get('https://yahoo.com') # Fake IO request
    return
