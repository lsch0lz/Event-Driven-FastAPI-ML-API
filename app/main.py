import uuid

from celery.result import AsyncResult
from fastapi import FastAPI, HTTPException

from app.core.celery_tasks.inference_task import celery_app, detect_class_in_image
from app.core.db.db import create_db_and_tables, SessionDependency
from app.core.db.inference_request import InferenceRequest

from app.core.models.job_status import JobStatus
from app.core.models.inference_job import InferenceJob
from app.core.models.result_request import ResultRequest

app = FastAPI()


# TODO: Use LifeSpan instead of on_event
@app.on_event("startup")
def create_db_tables():
    create_db_and_tables()


@app.post("/inference/", response_model=JobStatus)
async def create_inference_job(inference_job: InferenceJob) -> JobStatus:
    task = detect_class_in_image.delay(inference_job.model_dump())

    return JobStatus(id=task.id, status="PENDING")


@app.post("/results/", response_model=JobStatus)
def get_inference_result(result_request: ResultRequest, session: SessionDependency) -> JobStatus:
    result = celery_app.AsyncResult(result_request.task_id)

    if result.state == "PENDING":
        return JobStatus(id=result_request.task_id, status="PENDING")
    elif result.state == "SUCCESS":
        inference_request: InferenceRequest = InferenceRequest(
            id=uuid.uuid4(),
            customer_key=result_request.customer_key,
            request_time=1.0
        )
        session.add(inference_request)
        session.commit()
        session.refresh(inference_request)

        return JobStatus(id=result_request.task_id, status="SUCCESS", result=result.result)
    elif result.state == "FAILURE":
        return JobStatus(id=result_request.task_id, status="FAILURE", error=str(result.info))

    return JobStatus(id=result_request.task_id, status=result.state)

@app.get("/inference/{inference_id}")
def read_inference_request(inference_id: str, session: SessionDependency):
    inference_job = session.get(InferenceRequest, uuid.UUID(inference_id))
    if not inference_job:
        raise HTTPException(status_code=404, detail="InferenceResult not found")

    return inference_job

@app.get("/status", response_model=JobStatus)
def status(task_id: str) -> JobStatus:
    r = celery_app.AsyncResult(task_id)
    return JobStatus(id=r.task_id, status=r.status)
