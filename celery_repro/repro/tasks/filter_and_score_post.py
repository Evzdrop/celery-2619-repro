from celery import shared_task

from repro.monitoring.custom_metrics import custom_metric_timed_node, record_metric

import logging
import requests

logger = logging.getLogger(__name__)

@shared_task
@custom_metric_timed_node("Custom/filter_and_score_post/1")
def filter_and_score_post(post_pipeline_dto):
    requests.get('https://yahoo.com') # Fake IO request

    return ["scored post 1", "scored post 2", "scored post 3"]

