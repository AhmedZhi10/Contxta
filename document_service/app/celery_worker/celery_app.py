# in: app/celery_worker/celery_app.py

from celery import Celery
from app.core.config import settings

celery = Celery(
    __name__,
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

# --- THIS IS THE MAGIC LINE ---
# This tells the Celery worker to automatically discover and register any tasks
# defined in the 'app.celery_worker.tasks' module.
celery.autodiscover_tasks(['app.celery_worker'])


celery.conf.update(
    task_track_started=True,
)