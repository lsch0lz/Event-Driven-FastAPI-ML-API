from fastapi import APIRouter

from app.core.celery_tasks.inference_task import celery_app

from app.core.models.job_status import JobStatus

router = APIRouter(prefix="/status", tags=["status"])


@router.get("/", response_model=JobStatus)
def status(task_id: str) -> JobStatus:
    r = celery_app.AsyncResult(task_id)
    return JobStatus(id=r.task_id, status=r.status)
