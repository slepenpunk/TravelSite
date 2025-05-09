from celery import Celery

from config import REDIS_URL

celery = Celery(
    "tasks",
    broker=f"{REDIS_URL}",
    include=["tasks.tasks"],
    broker_connection_retry_on_startup=True,
)


celery.conf.update(
    accept_content=["json"],
    task_serializer="json",
    result_serializer="json",
)
