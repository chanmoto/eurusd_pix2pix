import pandas as pd
from ml.imagemake import GetSignal

from fastapi import APIRouter, Depends
from database import get_db
from sqlalchemy.orm import Session
from torchvision import transforms as transforms 
from ml.imagemake import   GetSignal
from backtesting import Strategy, Backtest
from crud.result_crud import get_result_span 
from crud.forex_crud import get_dataframe_date 
from datetime import datetime, timezone
from typing import Optional
from models.forex_model import Forex_short
import numpy as np
from configuration import IndicatorConfigurations as indc

# モジュール化する場合は、APIRouterのインスタンスを作る　→　命名はrouter
router = APIRouter(
    responses={404: {"forex": "Not found"}},
)

def func(data):
    return data.signal

class pix2pix(Strategy):

    def init(self):
        pass

    def next(self): #チャートデータの行ごとに呼び出される
        super().next()

        current_time = self.data.index[-1]
        self.signal1 = self.data.df['signal'][current_time]    
        #print(current_time,self.signal1)
        
        if self.signal1>10 and self.signal1<100:
            #self.position.close()
            #self.buy() # 買い
            self.sell()

        elif self.signal1>0.01 and self.signal1<0.1:
            #self.position.close()
            #self.sell()# 売り
            self.buy()
            
        # Additionally, set aggressive stop-loss on trades that have been open 
        # for more than two days
        for trade in self.trades:
            if current_time - trade.entry_time > pd.Timedelta(120, "m"):
                self.position.close()


@router.get("/backtest/")
async def backtes(db: Session = Depends(get_db),
    start_date: datetime =datetime.now(timezone.utc),
    end_date: datetime =datetime.now(timezone.utc)
    ):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    forex =  get_dataframe_date(db=db, model=Forex_short, start = start_date,  end = end_date)

    realdf = pd.DataFrame([[x.id,x.open,x.high,x.low,x.close,x.volume] for x in forex], columns=['id','Open','High','Low','Close','Volume'])

    realdf["id"] = pd.to_datetime(realdf["id"])
    realdf = realdf.set_index("id")
    realdf = realdf.sort_index()

    realdf['signal'] = -1.0

    Query = get_result_span(db,start_date,end_date)
    predict = pd.read_sql(sql=Query.statement, con = db.bind)
   
    for index, row in predict.iterrows():
        signal = GetSignal(row['fakeb'],indc)
        if row['id'] in realdf.index:
            realdf.at[row['id'], 'signal'] = signal
    
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