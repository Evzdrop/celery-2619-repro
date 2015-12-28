from celery import shared_task

# There's a convoluted bug in celery that prevents a task running with eventlet from
# queueing its results for a subsequent "group". Here's the issue to track it:
# https://github.com/celery/celery/issues/2619
#
# In the meantime, this is a workaround to allow IO-bound tasks to run on eventlet
# and queue results to a group through this task.

@shared_task()
def echo(arg, *args, **kwargs):
    return arg


