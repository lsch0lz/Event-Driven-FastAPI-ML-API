from celery.result import AsyncResult
from fastapi import FastAPI

from app.models.job_status import JobStatus
from app.celery_tasks.inference_task import add, celery_app

from app.models.inference_job import InferenceJob
from app.models.response import Response

app = FastAPI()


@app.post("/inference/", response_model=Response)
async def create_inference_job(inference_job: InferenceJob):
    result = add.delay(5,4)

    return Response(response_image=str(result.get(timeout=1)))

@app.get("/status", response_model=JobStatus)
def status(task_id: str) -> JobStatus:
    r = celery_app.AsyncResult(task_id)
    return JobStatus(id=r.task_id, status=r.status)
