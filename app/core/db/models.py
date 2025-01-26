import uuid

from sqlmodel import Field, SQLModel


class InferenceRequest(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    customer_key: str = Field(index=True)
    request_time: float = Field(default=None, index=True)

class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(index=True)
    password: str = Field(default=None)
    email: str = Field(index=True, default=None)
    full_name: str = Field(index=True, default=None)
    disabled: bool = Field(index=True, default=None)
