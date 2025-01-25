from typing import List

from celery.result import AsyncResult
from fastapi import FastAPI

from app.core.models.job_status import JobStatus
from app.core.celery_tasks.inference_task import celery_app, detect_class_in_image

from app.core.models.inference_job import InferenceJob
from app.core.models.result_request import ResultRequest

app = FastAPI()


@app.post("/inference/", response_model=JobStatus)
async def create_inference_job(inference_job: InferenceJob) -> JobStatus:
    task = detect_class_in_image.delay(inference_job.model_dump())

    return JobStatus(id=task.id, status="PENDING")


@app.post("/results/", response_model=JobStatus)
def get_inference_result(result_request: ResultRequest) -> JobStatus:
    result = celery_app.AsyncResult(result_request.task_id)

    if result.state == "PENDING":
        return JobStatus(id=result_request.task_id, status="PENDING")
    elif result.state == "SUCCESS":
        return JobStatus(id=result_request.task_id, status="SUCCESS", result=result.result)
    elif result.state == "FAILURE":
        return JobStatus(id=result_request.task_id, status="FAILURE", error=str(result.info))

    return JobStatus(id=result_request.task_id, status=result.state)


@app.get("/status", response_model=JobStatus)
def status(task_id: str) -> JobStatus:
    r = celery_app.AsyncResult(task_id)
    return JobStatus(id=r.task_id, status=r.status)
