# app/core/celery_app.py
from celery import Celery
from app.core.config import settings

celery = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["tasks.process"],  # Points to the file with your tasks
)
