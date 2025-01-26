import base64
import os
import time
from io import BytesIO
from typing import List, Dict

from celery import Celery
from ultralytics import YOLO
from PIL import Image

from app.core.models.inference_job import InferenceJob
from app.core.models.inference_response import Detection

celery_app = Celery("inference_task",
                    broker="pyamqp://guest@localhost//",
                    backend="redis://localhost:6379/0",
                    include=["app.core.celery_tasks.inference_task"])

celery_app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TIMEZONE='Europe/Oslo',
    CELERY_ENABLE_UTC=True
)

model = YOLO(os.getenv("ONNX_MODEL_PATH"), task="detect")


@celery_app.task
def detect_class_in_image(inference_job: InferenceJob):
    img = Image.open(BytesIO(base64.b64decode(inference_job["image_string"])))
    results = model(img)

    model_detections: List[Dict] = []
    for result in results:
        detection: Detection = Detection(boxes=result.boxes.xyxy.tolist()[0], confidence=result.boxes.conf.item(), label=result.boxes.cls.item())
        model_detections.append(detection.model_dump())

    return model_detections
