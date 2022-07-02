import datetime
import math
import re
import types
from typing import Any
from git import List
import numpy as np
import torch
from pandas import DataFrame as df
from PIL import Image
from torchvision import transforms
from configuration import IndicatorConfigurations as indc
import pdb

def getprice(img:List[Any], transform:Any, info:int,types:List[Any]):
    val={}
    for type in types:
        v = transform(Image.open(img[type]))
        v = v.numpy()

        #valueX = v[info, :, 0]
        valueXY = np.diag(v[info,:,:])
        #valueY = v[info, 0, :]
        #value = (valueX+valueY)/2
        val[type] = min_max(valueXY)
    #pdb.set_trace()
    return val, img['date']


def GetSignal(item,p:indc):

    y1 = np.mean(item[p.st1:p.ed1])
    y2 = np.mean(item[p.st2:p.ed2])
    return y2/y1


def min_max(x, axis=None):
    min = x.min(axis=axis, keepdims=True)
    max = x.max(axis=axis, keepdims=True)
    result = (x-min)/(max-min+0.0000000000010)
    return result

# データフレームから画像を作成
#box_size = 切り取りサイズ
# foot_slide　=　スライド幅

def imagemake(dfspan1: df,
              dfspan2: df,
              dfspan3: df,
              mode: str,
              size: int=64,
              slide: int=32
              ):

    wsize = int(math.pow(2, int(math.log2(size))))

    a = min_max(np.array([r.close for r in dfspan1]))
    b = min_max(np.array([r.close for r in dfspan2]))
    c = min_max(np.array([r.close for r in dfspan3]))

    m = np.outer(a, a).astype(np.float32)
    n = np.outer(b, b).astype(np.float32)
    o = np.outer(c, c).astype(np.float32)

    m1 = min_max(m[0:wsize, 0:wsize])
    m2 = min_max(m[slide:wsize+slide, slide:wsize+slide])
    n1 = min_max(n[0:wsize, 0:wsize])
    n2 = min_max(n[slide:wsize+slide, slide:wsize+slide])
    o1 = min_max(o[0:wsize, 0:wsize])
    o2 = min_max(o[slide:wsize+slide, slide:wsize+slide])

    te1 = np.stack([m1, n1, o1])
    te2 = np.stack([m2, n2, o2])

    te3 = np.concatenate([te1, te2], 2) if mode == 'A' \
        else np.concatenate([te2, te2], 2)
    a = 256/wsize, 256/wsize
    te4 = np.kron(te3, np.ones(tuple(map(int,a))))
    tmp = torch.from_numpy(te4).clone()

    return transforms.ToPILImage(mode='RGB')(tmp)

