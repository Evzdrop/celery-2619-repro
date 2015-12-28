import subprocess
import logging
import os
import time
from django.core.management.base import BaseCommand
from django.conf import settings

from repro.tasks.stream_chain import task_chain

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def handle(self, consumer=False, **kwargs):
        while True:
            task_chain('{"post": "post"}')
            time.sleep(3)

