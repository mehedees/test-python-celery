from celery import Celery


app = Celery(
    main="celery",
    broker="pyamqp://rabbitmq:rabbitmq1234@rabbitmq:5672//",
    backend="redis://redis:6379/0",
    include=['app.tasks']
)

app.conf.update(
    result_expires=3600,
)

