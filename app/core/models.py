from typing import Optional, Any, List

from pydantic import BaseModel


class InferenceJob(BaseModel):
    image_string: str


class Detection(BaseModel):
    boxes: List[float]
    confidence: float
    label: int


class JobStatus(BaseModel):
    id: str
    status: str
    result: Optional[Any] = None
    error: Optional[str] = None


class ResultRequest(BaseModel):
    task_id: str
    customer_key: str
