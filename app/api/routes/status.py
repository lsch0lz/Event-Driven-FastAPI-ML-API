from fastapi import APIRouter, Depends

from app.core.auth.security import get_current_active_user
from app.core.celery_tasks.inference_task import celery_app

from app.core.models.job_status import JobStatus

router = APIRouter(prefix="/status", tags=["status"])


@router.get("/", dependencies=[Depends(get_current_active_user)], response_model=JobStatus)
def status(task_id: str) -> JobStatus:
    r = celery_app.AsyncResult(task_id)
    return JobStatus(id=r.task_id, status=r.status)
