from pydantic import BaseModel


class ResultRequest(BaseModel):
    task_id: str
    customer_key: str
