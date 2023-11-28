import os
from celery import Celery

def create_celery():
    celery = Celery(__name__)
    celery.conf.broker_url = os.environ.get("CELERY_BROKER", "redis://localhost:6379")

    return celery

celery = create_celery()

