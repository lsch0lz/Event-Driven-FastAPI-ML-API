import uuid
from fastapi import APIRouter, HTTPException, Depends

from app.core.auth.security import get_current_active_user
from app.core.celery_tasks.inference_task import celery_app, detect_class_in_image

from app.core.models import JobStatus, InferenceJob

from app.core.db.database import create_db_and_tables, SessionDependency
from app.core.db.models import InferenceRequest

router = APIRouter(prefix="/inference", tags=["inference"])

@router.post("/", dependencies=[Depends(get_current_active_user)], response_model=JobStatus)
async def create_inference_job(inference_job: InferenceJob) -> JobStatus:
    task = detect_class_in_image.delay(inference_job.model_dump())

    return JobStatus(id=task.id, status="PENDING")

@router.get("/{inference_id}", dependencies=[Depends(get_current_active_user)])
def read_inference_request(inference_id: str, session: SessionDependency):
    inference_job = session.get(InferenceRequest, uuid.UUID(inference_id))
    if not inference_job:
        raise HTTPException(status_code=404, detail="InferenceResult not found")

    return inference_job

@router.delete("/{inference_id}", dependencies=[Depends(get_current_active_user)])
def delete_inference_request(inference_id: str, session: SessionDependency):
    inference_job = session.get(InferenceRequest, uuid.UUID(inference_id))
    if not inference_job:
        raise HTTPException(status_code=404, detail="InferenceResult not found")

    session.delete(inference_job)
    session.commit()

    return {"OK": True}