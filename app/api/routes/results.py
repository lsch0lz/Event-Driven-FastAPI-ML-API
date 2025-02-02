import uuid

from fastapi import APIRouter, HTTPException

from app.core.celery_tasks.inference_task import celery_app

from app.core.db.db import SessionDependency
from app.core.db.inference_request import InferenceRequest

from app.core.models.job_status import JobStatus
from app.core.models.result_request import ResultRequest

router = APIRouter(prefix="/results", tags=["results"])

@router.post("/", response_model=JobStatus)
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
