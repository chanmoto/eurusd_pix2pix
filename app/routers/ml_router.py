from enum import Enum
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Query
from database import get_db
from ml.pix2pix import image_set_ready, get_result_ready,plot_result_ready_bb
from ml.cmd import train, test
from configuration import MachineLearningConfigurations as MLConfig
import pdb
from models.result_model import ResultBase 
from datetime import datetime, timezone

model = ResultBase()

# モジュール化する場合は、APIRouterのインスタンスを作る　→　命名はrouter
router = APIRouter(
    responses={
        418: {"description": "I'm a ml router"},
        404: {"ml_router": "Not found"}
    }
)

"""
教師データを作成するAPI
引数：
db: Session
framesize: 箱サイズ
slide: 箱スライド量
mode: Predict_mode　フォルダ名を指定 --->　test,val,train
start: 取得開始日
count: 取得件数
"""


@router.get("/imagemake/")
async def get_predict(db: Session = Depends(get_db),
                      count: int = 1,
                      size: int = 64,
                      slide: int = 32,
                      mode: str = Query("A", enum=["A", "B"]),
                      target: str = Query(list(MLConfig.paths.keys())[0],
                                          enum=list(MLConfig.paths.keys()))
                      ):
    return {"imagemake was finished": image_set_ready(
        db=db,
        count=count,
        target=target,
        mode=mode,
        size=size,
        slide=slide
    )}

"""
PIX2PIXで訓練するAPI
引数：
db: Session
framesize: 箱サイズ
slide: 箱スライド量
mode: Predict_mode　　　フォルダ名を指定 --->　test,val,train
start: 取得開始日
count: 取得件数
"""


@router.get("/train/")
def get_train(
    db: Session = Depends(get_db),
    param: str = Query("",
                       enum=["--continue", ""])
):
    return {'msg': train(Continue=param)}


@router.get("/test/")
def get_test(
    db: Session = Depends(get_db),
    phase: str = Query(list(MLConfig.paths.keys())[0],
                       enum=list(MLConfig.paths.keys())),
    number: int = 1
):
    print(phase)
    return test(Phase=phase,number=number)

@router.get("/result/")
def get_result(
    db: Session = Depends(get_db),
    phase: str = Query(list(MLConfig.paths.keys())[0],
                       enum=list(MLConfig.paths.keys())),
                       info:int=0
):
    return get_result_ready(db=db,phase=phase,info=    info,shift=128)

@router.get("/plot/")
async def get_plot(
    
    db: Session = Depends(get_db),
    phase: str = Query(list(MLConfig.paths.keys())[0],
                       enum=list(MLConfig.paths.keys())),
    start_date: datetime =datetime.now(timezone.utc),
    end_date: datetime =datetime.now(timezone.utc)
    
):
    return {'msg': plot_result_ready_bb(db=db,phase=phase,start=start_date,end=end_date)}