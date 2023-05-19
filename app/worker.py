import os
from celery import Celery
from celery.signals import worker_process_shutdown, worker_ready

from .db_client import connect_to_db_sync, shutdown_db_sync, db


# def find_tasks() -> list[str]:
#     curr_dir =


@worker_ready.connect
def db_conn_init(*args, **kwargs):
    """ Initialize a clean DB connection. """
    if db.cluster is not None:
        shutdown_db_sync()
    connect_to_db_sync()


@worker_process_shutdown.connect
def cassandra_shutdown(*args, **kwargs):
    """Close DB connection"""
    shutdown_db_sync()


CELERY_BROKER: str = (
    f"pyamqp://user:Pass1234@rabbitmq:5672//"
)
CELERY_BACKEND: str = f"redis://redis:6379"
celery_app = Celery(
    __name__, broker=CELERY_BROKER, backend=CELERY_BACKEND
)


celery_app.conf.broker_pool_limit = 500
celery_app.conf.worker_prefetch_multiplier = 5
celery_app.conf.worker_send_task_events = False
celery_app.conf.task_send_sent_event = False
celery_app.conf.task_ignore_result = True
celery_app.conf.task_store_errors_even_if_ignored = True
celery_app.conf.result_expires = 30


celery_app.autodiscover_tasks(packages=['app'])
