# backend/app/tasks/celery_app.py
from celery import Celery
from app.config import settings

celery_app = Celery(
    "autopost_tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.pipeline", "app.tasks.scheduler"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
)

celery_app.conf.beat_schedule = {
    "publish-scheduled-posts-every-5-min": {
        "task": "publish_scheduled_posts",
        "schedule": 300.0,
    },
}
