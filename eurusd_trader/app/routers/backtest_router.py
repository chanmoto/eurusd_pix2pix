import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm
from ml.imagemake import getprice,GetSignal,GetResultsImgs
from configuration import MachineLearningConfigurations as MLConfig
from fastapi import APIRouter, Depends, Body
from database import get_db
from sqlalchemy.orm import Session
from torchvision import transforms as transforms 
from ml.imagemake import imagemake, getprice, GetSignal
from backtesting import Strategy, Backtest
from models.result_model import Results

import pdb

# モジュール化する場合は、APIRouterのインスタンスを作る　→　命名はrouter
router = APIRouter(prefix="/backtest",
    tags=["v1"],
    responses={404: {"forex": "Not found"}},
)

class pix2pix(Strategy):

    def init(self):
        self.signal1 = self.data.signal
        pass
    
    def next(self): #チャートデータの行ごとに呼び出される
        super().next()

        current_time = self.data.index[-1]
            
        if self.signal1>5 and self.signal1<100:
            #self.position.close()
            self.buy() # 買い
            
        elif self.signal1>0.001 and self.signal1<0.2:
            #self.position.close()
            self.sell()# 売り
    
        # Additionally, set aggressive stop-loss on trades that have been open 
        # for more than two days
        for trade in self.trades:
            if current_time - trade.entry_time > pd.Timedelta(5, "m"):
                self.position.close()
                    
@router.get("/backtest/")
async def backtes(db: Session = Depends(get_db)):

    pdb.set_trace()
    realdf = pd.read_csv(r'C://Users//User//Desktop//EURUSD.oj5k5.csv', sep=",",names=('date', 'time', 'Open', 'High', 'Low', 'Close', 'Volume'))
    realdf.index = pd.to_datetime(realdf['date']+" "+realdf['time'])
    realdf['signal']=-1

    img = GetResultsImgs()

    transform = transforms.PILToTensor()
    for item in img:
        v2, date = getprice(item, transform, 0)
        signal = GetSignal(v2)
        realdf.at[date, 'signal'] = signal

    bt = Backtest(
    realdf, # チャートデータ
    pix2pix, # 売買戦略
    cash=100000, # 最初の所持金
    commission=0.000, # 取引手数料
    margin=0.5, # レバレッジ倍率の逆数（0.5で2倍レバレッジ）
    trade_on_close=True, # True：現在の終値で取引，False：次の時間の始値で取引
    exclusive_orders=True #自動でポジションをクローズ
    )

    output = bt.run() # バックテスト実行
    print(output) # 実行結果(データ)
    bt.plot() # 実行結果（グラフ）