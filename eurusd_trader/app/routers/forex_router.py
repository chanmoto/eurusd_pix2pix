from fastapi import Depends, Body, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from models.forex_model import Forex2_m5,Forex2_m30,Forex2_m240
from datetime import datetime as dt
from crud.forex_crud import get_last_time, add_forex
from schemas import forex_schema as schema
import pdb

# モジュール化する場合は、APIRouterのインスタンスを作る　→　命名はrouter
router = APIRouter(
    responses={404: {"forex": "Not found"}},
)

def session_clear(exception):
    if exception and Session.is_active:
        Session.rollback()
    else:
        pass
    Session.close()

@router.get("/getlasttime/")
async def gettime(db: Session = Depends(get_db),):
    return {
        "m5": get_last_time(db=db,model=Forex2_m5),
        "m30": get_last_time(db=db,model=Forex2_m30),
        "m240": get_last_time(db=db,model=Forex2_m240)
    }

@router.post("/gettick/")
async def gettick(
        db: Session = Depends(get_db),
        body=Body(...)):

    time, peristr, open, high, low, close, volume = body["content"].split(",")

    obj =schema.Forex(
            id = dt.strptime(time, "%Y.%m.%d %H:%M"),    
            open = open,
            high= high,
            low= low,
            close= close,
            volume= volume
    )
    if peristr == "forex_f1":
        repo = Forex2_m5
    elif peristr == "forex_f2":
        repo = Forex2_m30
    elif peristr == "forex_f3":
        repo = Forex2_m240
    else:
        return {"error": "invalid peristr"}
    
    try:    
        r = add_forex(
        db=db,
        schema = obj,
        model = repo,
        commit=True,
        )

    except Exception as e:
        session_clear(e)
        return {"error": "invalid data"}

    return {"msg": "data posting comleted" }
