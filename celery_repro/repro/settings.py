import os

from kombu.common import Broadcast

ENV = os.environ.get('ENV', 'local')
GIT_REVISION = os.environ.get('GIT_REVISION', '')

"""
Django settings for repro project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
import djcelery
djcelery.setup_loader()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import pwd
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

import uuid

MACHINE_NAME = os.environ.get('MACHINE_NAME', 'undefined')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '16+s9*zvapmn6e4hx8h_&y&ad9&&nt18lwv%ca0e39070^zc0c'

# SECURITY WARNING: don't run with debug turned on in production!
if ENV in ['dev', 'local']:
    DEBUG = True
    TEMPLATE_DEBUG = True
else:
    DEBUG = False

RECORD_METRICS = os.environ.get('RECORD_METRICS')

# this setting is only observed if DEBUG=False
ALLOWED_HOSTS = ['*',]

RABBIT_ADMIN_PROTOCOL = 'https'
if ENV in ['local']:
    RABBIT_ADMIN_PROTOCOL = 'http'

RABBIT_USER = os.environ.get('RABBIT_USER', 'guest')
RABBIT_PASSWORD = os.environ.get('RABBIT_PASSWORD', 'guest')
RABBIT_DOMAIN = os.environ.get('RABBIT_DOMAIN', 'localhost')
RABBIT_PORT = os.environ.get('RABBIT_PORT', 5672)
RABBIT_ADMIN_PORT = os.environ.get('RABBIT_ADMIN_PORT', 15672)
RABBIT_VHOST = os.environ.get('RABBIT_VHOST', '')
RABBIT_URI = os.environ.get('RABBIT_URI', 'amqp://%s:%s@%s:%s/%s'%(RABBIT_USER,RABBIT_PASSWORD,RABBIT_DOMAIN,RABBIT_PORT,RABBIT_VHOST))
BROKER_URL = RABBIT_URI

import jsonpickle
from kombu.serialization import BytesIO, register
from io import StringIO

def json_decode(input):
    byte_stream = BytesIO(input)
    stringified = None
    try:
        stringified = byte_stream.getvalue()
    finally:
        byte_stream.close()

    return jsonpickle.decode(stringified)

register('jsonpickle', jsonpickle.encode, json_decode,
    content_type='application/json',
    content_encoding='utf-8')

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'jsonpickle'
CELERY_RESULT_SERIALIZER = 'jsonpickle'
CELERY_ANNOTATIONS = {}
CELERY_ALWAYS_EAGER = False
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
CELERY_ACKS_LATE = True
CELERYD_PREFETCH_MULTIPLIER = 1

from kombu import Exchange, Queue
default_exchange = Exchange('repro_exchange', type='direct')
CELERY_QUEUES = (
    Queue('repro_incoming_twitter', routing_key='repro_twitter'),
    Queue('repro_filter_and_score_post', routing_key='repro_filter_and_score_post'),
    Queue('repro_conversations', routing_key='repro_convo'),
    Queue('repro_echo', routing_key='repro_echo'),
)
CELERY_DEFAULT_EXCHANGE = 'repro_exchange'
CELERY_DEFAULT_QUEUE = 'repro'
CELERY_DEFAULT_ROUTING_KEY = ''

# routing for celery tasks
CELERY_ROUTES = {
    'repro.tasks.incoming.incoming': {
        'queue': 'repro_incoming_twitter',
        'routing_key': 'repro_twitter'
    },
    'repro.tasks.filter_and_score_post.filter_and_score_post': {
        'queue': 'repro_filter_and_score_post',
        'routing_key': 'repro_filter_and_score_post'
    },
    'repro.tasks.associate_conversations.associate_conversations': {
        'queue': 'repro_conversations',
        'routing_key': 'repro_convo'
    },
    'repro.tasks.echo.echo': {
        'queue': 'repro_echo',
        'routing_key': 'repro_echo'
    }
}

USER_NAME = pwd.getpwuid(os.getuid()).pw_name or 'unknown'

# Application definition

INSTALLED_APPS = (
    'repro',
)

MIDDLEWARE_CLASSES = (
)

AUTHENTICATION_BACKENDS = (
)

ROOT_URLCONF = 'repro.urls'

WSGI_APPLICATION = 'repro.wsgi.application'

REDIS = {
    'host': 'localhost',
    'port': '6379'
}

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ.get('DB_NAME', 'test'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'USER': os.environ.get('DB_USER', 'test'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'test')
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT= os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = (
    os.path.join(
        BASE_DIR, '..', 'client', 'dist', 'client'
    ),
)

# API Settings

# adapted from DEFAULT_LOGGING in django.utils.log
LOGGING = {
    'version': 1,
    # disables traditional django logging. if you expect to see something and don't
    # this is probably why.
    'disable_existing_loggers': True,
    'handlers': {
        # removed require_debug_true because prod uses supervisor to handle stdout.
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
        'null': {
            'class': 'logging.NullHandler',
        }
    },
    'formatters': {
        'default': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(message)s'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'celery': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'django.security': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'py.warnings': {
            'handlers': ['console'],
        },
        'repro': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}


# Admin configuration
ADMIN_SITE_TITLE = ADMIN_SITE_HEADER = 'Earshot Core Admin'

CELERY_RESULT_BACKEND = 'redis://%s:%s/'%(REDIS['host'], REDIS['port'])
CELERY_IGNORE_RESULT = True
CELERY_CHORD_PROPAGATES = True
