from typing import List

from pydantic import BaseModel

class Detection(BaseModel):
   boxes: List[float]
   confidence: float
   label: int

class InferenceResponse(BaseModel):
   detections: List[Detection]
