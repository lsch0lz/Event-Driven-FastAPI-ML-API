from pydantic import BaseModel


class JobStatus(BaseModel):
    id: str
    status: str