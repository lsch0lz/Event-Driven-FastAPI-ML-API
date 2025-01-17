from typing import Optional, Any

from pydantic import BaseModel


class JobStatus(BaseModel):
    id: str
    status: str
    result: Optional[Any] = None
    error: Optional[str] = None