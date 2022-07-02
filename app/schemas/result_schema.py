from datetime import datetime
from pydantic import BaseModel
from typing import List, Dict, Optional


class Result(BaseModel):
    id : datetime
    reala: List[float]
    realb: List[float]
    fakeb: List[float]
    signal: float
 
    class Config:
        orm_mode = True
