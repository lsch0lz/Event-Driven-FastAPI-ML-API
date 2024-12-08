import time

from celery import Celery

celery_app = Celery("inference_task", broker="pyamqp://guest@localhost//", backend="rpc://guest@localhost//",
                    include=["app.celery_tasks.inference_task"])

celery_app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TIMEZONE='Europe/Oslo',
    CELERY_ENABLE_UTC=True
)


@celery_app.task
def add(x, y):
    time.sleep(20)
    return x + y
