import requests
from celery import shared_task

from django.utils import timezone

@shared_task
def associate_conversations(post_pipeline_dto):
    requests.get('https://yahoo.com') # Fake IO request

    requests.get('https://yahoo.com') # Fake IO request

    requests.get('https://yahoo.com') # Fake IO request

    return post_pipeline_dto
