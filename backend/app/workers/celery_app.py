"""
Celery application configuration.

This module centralizes Celery configuration for:
- ingestion workers
- embedding workers
- AI processing tasks

IMPORTANT:
RabbitMQ is intentionally used as the broker to support
distributed async processing at enterprise scale.
"""

from celery import Celery


celery_app = Celery(
    "optica_workers",
    broker="amqp://guest:guest@rabbitmq:5672//",
    backend="rpc://",
)


celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# celery_app.autodiscover_tasks(
#     [
#         "app.workers",
#     ]
# )

from app.workers import ingestion,embedding
