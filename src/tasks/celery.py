from celery import Celery

from config import REDIS_URL

celery = Celery(
    "tasks",
    broker=f"{REDIS_URL}",
    include=["tasks.tasks"],
    broker_connection_retry_on_startup=True,
)

# In your Celery config file (usually celery.py or app.py)
celery.conf.update(
    accept_content=['json'],  # Only accept JSON serialization
    task_serializer='json',
    result_serializer='json',
)
