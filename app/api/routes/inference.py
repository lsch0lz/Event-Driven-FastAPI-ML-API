import uuid
from fastapi import APIRouter, HTTPException

from app.core.celery_tasks.inference_task import celery_app, detect_class_in_image

from app.core.models.job_status import JobStatus
from app.core.models.inference_job import InferenceJob

from app.core.db.db import create_db_and_tables, SessionDependency
from app.core.db.inference_request import InferenceRequest

router = APIRouter(prefix="/inference", tags=["inference"])

@router.post("/", response_model=JobStatus)
async def create_inference_job(inference_job: InferenceJob) -> JobStatus:
    task = detect_class_in_image.delay(inference_job.model_dump())

    return JobStatus(id=task.id, status="PENDING")

@router.get("/{inference_id}")
def read_inference_request(inference_id: str, session: SessionDependency):
    inference_job = session.get(InferenceRequest, uuid.UUID(inference_id))
    if not inference_job:
        raise HTTPException(status_code=404, detail="InferenceResult not found")

    return inference_job

@router.delete("/{inference_id}")
def delete_inference_request(inference_id: str, session: SessionDependency):
    inference_job = session.get(InferenceRequest, uuid.UUID(inference_id))
    if not inference_job:
        raise HTTPException(status_code=404, detail="InferenceResult not found")

    session.delete(inference_job)
    session.commit()

    return {"OK": True}