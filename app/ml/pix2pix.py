from datetime import datetime
import pdb
import os
import re
import shutil

import numpy as np
from configuration import MachineLearningConfigurations as MLConfig
from models.forex_model import Forex_short, Forex_middle, Forex_long
from sqlalchemy.orm import Session
from tqdm import tqdm
import math
import pickle
from torchvision import transforms
from schemas import result_schema as schemas
from crud import result_crud as result 
from crud import forex_crud as forex 
from ml.imagemake import imagemake, getprice, GetSignal
import matplotlib.pyplot as plt
from configuration import IndicatorConfigurations as indc
# データベースをまさぐり、PIX2PIX用のデータを作成する
# データタイプとしては、TRAINはTESTと、VALを分けたほうが良い
# 予測に関しては、データの固め方の問題　A（前半）にするか、B（後半）
# wsizeは、窓の寸法
# slideは、窓のずらし量



def pix2image(
    db: Session,
    count_max: int = 100,
    mode: str = "A",  # 訓練時はAとする。予測の場合はBとする。
    target: str = "train",  # train or test
    size: int = 64,
    slide: int = 32
):

    models=Forex_short, Forex_middle, Forex_long
    start = forex.get_datafrom_endpoint(db=db, framesize=count_max,models=models)

    print("start : {}".format(start))

    imgs = []
    count = 0
    min2pow = int(math.pow(2, int(math.log2(size))))
    df_length = min2pow+slide
    #pdb.set_trace()

    for t in tqdm(forex.get_dataframe_all(db=db,model=Forex_short)):
        if t.id <= start:
            dt = t.id
            df11 = forex.get_dataframe_span(
                db=db, framesize=df_length, dt=dt,model = Forex_short) 
            df22 = forex.get_dataframe_span(
                db=db, framesize=df_length,  dt=dt,model = Forex_middle) 
            df33 = forex.get_dataframe_span(
                db=db, framesize=df_length, dt=dt,model = Forex_long)

            if len(df11) == df_length and len(df22) == df_length and len(df33) == df_length:
                
                img = imagemake(df11, df22, df33, size=min2pow, slide=slide,mode=mode)
                fname = MLConfig.paths[target] + \
                dt.strftime('%Y-%m-%d %H_%M_00') + '.png'

                img.save(fname)
                imgs.append({"img": img, "fname": fname, "date": dt})
                count += 1
                if count >= count_max:
                    break
    return count,imgs


def rmdir(path: str = ""):
    shutil.rmtree(path)
    os.mkdir(path)
    print("Delete folder : {}".format(dir))
    return

def image_set_ready(db:Session ,target:str,count:int,mode:str,size:int,slide:int):
    rmdir(MLConfig.paths[target])
    c,imgs = pix2image(db=db, count_max=count, mode=mode, size=size, slide=slide,target=target)

    return "imagedata was pickled : n={}".format(c)
    

def GetResultsImgs(db: Session,phase:str):
    #pdb.set_trace()
    img = []
    image = {}
    path = os.path.join(MLConfig.result_dir + "{}_latest/images/".format(phase))
    
    if not os.path.isdir(path):
        print("No such directory : {}".format(path))
        return False

    print(path)

    for imageName in os.listdir(path):
        inputPath = os.path.join(path, imageName)
        if "fake_B" in imageName:
            image['fakeb'] = inputPath
        if "real_A" in imageName:
            image['reala'] = inputPath
        if "real_B" in imageName:
            image['realb'] = inputPath
        if len(image) == 3:
            ddd = re.findall(r"\d\d\d\d-\d\d-\d\d \d\d_\d\d_\d\d", inputPath)

            try: 
                image['date'] = ddd[0].replace("_", ":")
                img.append(image)
                image = {}
            except:
                pass
   
    return img


def get_result_ready(db: Session,phase:str,info:int,shift:int):

    img = GetResultsImgs(db=db,phase=phase)
    #pdb.set_trace()
    
    transform = transforms.PILToTensor()
    signal = None

    for item in tqdm(img):
        v2, d = getprice(item, transform, info,['reala','realb','fakeb'])
        
        signal = GetSignal(v2['fakeb'],indc)
        #pdb.set_trace()
        results = schemas.Result(
            id=d,
            reala=v2["reala"].tolist(),
            realb=v2['realb'].tolist(),
            fakeb=v2['fakeb'].tolist(),
            signal=signal
        )   
        result.add(db=db,obj=results)
    
        title = "{} {}".format(results.id,signal)
        plt.title(title)

        head = results.reala    
        tail = results.realb
        tail2 = results.fakeb

        head_range = np.max(head[128:256])- np.min(head[128:256])
        tail_range = np.max(tail[0:128])- np.min(tail[0:128])
        tail2_range = np.max(tail2[0:128])- np.min(tail2[0:128])

        tail = tail / ( tail_range / head_range )
        tail2 = tail2 / ( tail2_range / head_range )

        head_average = np.mean(head[128:256])
        tail_average = np.mean(tail[0:128])
        tail2_average = np.mean(tail2[0:128])
    
        head= head-head_average
        tail= tail-tail_average
        tail2= tail2-tail2_average
        
        im1 = plt.plot(np.append(head , [0] * shift ))
        #im2 = plt.plot(np.append([0] * shift  , tail))
        im3 = plt.plot(np.append([0] * shift  , tail2))
        #im3 = plt.plot(([0] * shift)  + results.realb)

        plt.show()
        plt.close()
    
    return signal


def plot_result_ready(db: Session,phase:str):
    
    objs = result.select_all(db=db)
    
    for obj in objs:
        pdb.set_trace()
        title = "{}".format(obj.id)
        plt.title(title)
        im1 = plt.plot(obj.reala+([0] * 64) )
        im2 = plt.plot(([0] * 64)  + obj.fakeb)
        im3 = plt.plot(([0] * 64)  + obj.realb)

        plt.show()


def plot_result_ready_bb(db: Session,phase:str,start:datetime,end:datetime):
    obj = result.select_all(db=db,start=start,end=end)
    try:
        title = "{}".format(obj.id)
        plt.title(title)
        im1 = plt.plot([0] * 128 + obj.realb)
        im2 = plt.plot([0] * 128 + obj.fakeb)
        im3 = plt.plot(obj.reala + [0] * 128 )
        plt.show()
    except:
        pass
    



        