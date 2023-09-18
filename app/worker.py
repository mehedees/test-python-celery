from celery import Celery
from celery.schedules import crontab


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


# Autodiscovery of defined tasks
celery_app.autodiscover_tasks(packages=['app'])

celery_app.conf.timezone = 'Asia/Dhaka'
celery_app.conf.beat_schedule = {
    'email_sending_task_0930_hour': {  # this key name doesn't mean anything
        'task': 'tasks.send_weekly_newsletter_email_task',
        'schedule': crontab(hour=9, minute=30, day_of_week=1),
        'args': ()
    },
    'news_collecting_task_every_24_hours': {
        'task': 'tasks.collect_daily_news_for_newsletter_task',
        'schedule': 86400,  # every 24*60*60 seconds,
        'args': ()
    }
}
