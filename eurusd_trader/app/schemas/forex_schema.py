from datetime import datetime
from pydantic import BaseModel

class Forex(BaseModel):
    id : datetime
    open:float
    high:float
    low:float
    close:float
    volume:float

    class Config:
        orm_mode = True
