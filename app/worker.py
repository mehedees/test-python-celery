from celery import Celery


# Broker(RabbitMQ) connection str
CELERY_BROKER: str = (
    f"pyamqp://user:Pass1234@rabbitmq:5672//"
)

# Result Backend(Redis) connection str
CELERY_BACKEND: str = f"redis://redis:6379"


# Celery App instance
celery_app = Celery(
    __name__, broker=CELERY_BROKER, backend=CELERY_BACKEND
)


celery_app.conf.worker_send_task_events = False
celery_app.conf.task_send_sent_event = False

# Autodiscovery of defined tasks
celery_app.autodiscover_tasks(packages=['app'])
