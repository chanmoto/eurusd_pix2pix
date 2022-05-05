import pandas as pd
import os
from database import engine
 
os.environ['KMP_DUPLICATE_LIB_OK']='True'

def load_csv():
    df1 = pd.read_csv(r'C://Users//User//Desktop//EURUSD.oj5k5.csv', sep=",",names=('date', 'time', 'open', 'high', 'low', 'close', 'volume'))
    df1.index = pd.to_datetime(df1['date']+" "+df1['time'])
    df1 = df1.drop(['date', 'time'], axis=1)

    df2 = pd.read_csv(r'C://Users//User//Desktop//EURUSD.oj5k30.csv', sep=",",names=('date', 'time', 'open', 'high', 'low', 'close', 'volume'))
    df2.index = pd.to_datetime(df2['date']+" "+df2['time'])
    df2 = df2.drop(['date', 'time'], axis=1)

    df3 = pd.read_csv(r'C://Users//User//Desktop//EURUSD.oj5k240.csv', sep=",",names=('date', 'time', 'open', 'high', 'low', 'close', 'volume'))
    df3.index = pd.to_datetime(df3['date']+" "+df3['time'])
    df3 = df3.drop(['date', 'time'], axis=1)

    df1.to_sql("forex2_m5", con=engine, index=True, index_label='id', if_exists='replace')
    df2.to_sql("forex2_m30", con=engine, index=True, index_label='id', if_exists='replace')
    df3.to_sql("forex2_m240", con=engine, index=True, index_label='id', if_exists='replace')

    
def initialize():
    print('Initialize the dataframe.')
    load_csv()
    print('done')