from datetime import datetime
from pydantic import BaseModel
from typing import List, Dict, Optional


class Result(BaseModel):
    id : datetime
    realA: List[float]
    realB: List[float]
    fakeB: List[float]
    signal: float
 
    class Config:
        orm_mode = True
