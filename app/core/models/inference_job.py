from pydantic import BaseModel

class InferenceJob(BaseModel):
    image_string: str
