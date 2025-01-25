import uuid

from sqlmodel import Field, SQLModel


class InferenceRequest(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    customer_key: str = Field(index=True)
    request_time: float = Field(default=None, index=True)
