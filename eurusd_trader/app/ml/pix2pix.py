import pdb
import os
import re
import shutil

from configuration import MachineLearningConfigurations as MLConfig
from models.forex_model import Forex2_m5, Forex2_m30, Forex2_m240,Forex
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
    models=Forex2_m5, Forex2_m30, Forex2_m240
    start = forex.get_datafrom_endpoint(db=db, framesize=count_max,models=models)

    print("start : {}".format(start))

    imgs = []
    count = 0
    min2pow = int(math.pow(2, int(math.log2(size))))
    df_length = min2pow+slide

    for t in tqdm(forex.get_dataframe_all(db=db,model=Forex2_m5)):
        if t.id <= start:
            dt = t.id
            df11 = forex.get_dataframe_span(
                db=db, framesize=df_length, dt=dt,model = Forex2_m5) 
            df22 = forex.get_dataframe_span(
                db=db, framesize=df_length,  dt=dt,model = Forex2_m30) 
            df33 = forex.get_dataframe_span(
                db=db, framesize=df_length, dt=dt,model = Forex2_m240)

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

    return {"msg" : "imagedata was pickled : n={}".format(c)}
    

def GetResultsImgs(db: Session,phase:str):
    img = []
    image = {}
    path = os.path.join(MLConfig.result_dir + "{}_latest/images/".format(phase))
    print(path)

    for imageName in os.listdir(path):
        inputPath = os.path.join(path, imageName)
        if "fake_B" in imageName:
            image['fakeB'] = inputPath
        if "real_A" in imageName:
            image['realA'] = inputPath
        if "real_B" in imageName:
            image['realB'] = inputPath
        if len(image) == 3:
            ddd = re.findall(r"\d\d\d\d-\d\d-\d\d \d\d_\d\d_\d\d", inputPath)

            try: 
                image['date'] = ddd[0].replace("_", ":")
                img.append(image)
                image = {}
            except:
                pass
   
    return img


def get_result_ready(db: Session,phase:str):

    img = GetResultsImgs(db=db,phase=phase)
    transform = transforms.PILToTensor()

    for item in img:
        v2, d = getprice(item, transform, 0,['realA','realB','fakeB'])
        signal = GetSignal(v2['fakeB'])
        
        results = schemas.Result(
            id=d,
            realA=v2["realA"].tolist(),
            realB=v2['realB'].tolist(),
            fakeB=v2['fakeB'].tolist(),
            signal=signal
        )
        print(results.id)
        result.add(db=db,obj=results)
    
    return {"msg", "pass2"}


def plot_result_ready(db: Session,phase:str):

    objs = result.select_all(db=db)
    
    for obj in objs:
        plt.title(obj.id) 
        im1 = plt.plot(obj.realB)
        im2 = plt.plot(obj.fakeB)
        plt.show()
