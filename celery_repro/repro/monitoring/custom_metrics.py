import functools
import requests
import time

from django.conf import settings

class CustomMetricTimedNode(object):

    def __init__(self, name):
        self.name = name
        self.start_time = None
        self.end_time = None

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc, value, tb):
        if not self.start_time:
            return
        self.end_time = time.time()
        duration = self.end_time - self.start_time

        requests.get('https://yahoo.com') # Fake IO request

def custom_metric_timed_node(name):
    def _decorator(f):
        @functools.wraps(f)
        def _wrapper(*args, **kwargs):
            with CustomMetricTimedNode(name):
                return f(*args, **kwargs)
        return _wrapper
    return _decorator


def record_metric(name, value):
    requests.get('https://yahoo.com') # Fake IO request
