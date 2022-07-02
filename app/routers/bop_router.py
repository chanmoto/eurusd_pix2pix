from fastapi import APIRouter
from torchvision import transforms as transforms 
from services.selenium import Selenium  

# モジュール化する場合は、APIRouterのインスタンスを作る　→　命名はrouter
router = APIRouter(
    responses={404: {"bop": "Not found"}},
)

try:
    b = Selenium()
except:
    Selenium.x()
    quit()

@router.get("/order/")
async def order(signal1 : float):
        if signal1>0.01 and signal1<0.166:
            b.s(0.5)
            b.purchase("high")
            b.s(0.5)
            
        elif signal1>8 and signal1<100:
            b.s(0.5)
            b.purchase("low")
            b.s(0.5)
    
        return {"ordered":str(signal1)}

