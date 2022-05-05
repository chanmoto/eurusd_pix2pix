from pyexpat import model
from sqlalchemy import Column, Integer, Float, DateTime, func
from database import Base
from sqlalchemy.orm import Session
from sqlalchemy_utils import get_class_by_table
from sqlalchemy import desc
from datetime import datetime
from models import forex_model as model_
from schemas import forex_schema as schema_
from models.forex_model import Forex
import pdb


def get_last_time(db: Session,model:model_.Forex):

    try:
        q = db.query(func.max(model.id).label('id_max')).subquery('sub1')
        r = db.query(model).filter(model.id == q.c.id_max).all()

        return str(r[0].id).replace("-", ".")
    except:
        pass


def get_dataframe(db: Session, framesize: int,model:model_.Forex):

    try:
        q = db.query(model).distinct(model.id).order_by(
            desc(model.id)).limit(framesize).subquery('sub1')
        r = db.query(model).filter(
            model.id == q.c.id).order_by(model.id).all()
        return r
    except:
        pass


def get_dataframe_all(db: Session,model:model_.Forex):
    try:
        q = db.query(model).distinct(
            model.id).order_by(desc(model.id)).all()
        return q
    except:
        pass


def get_dataframe_span(db: Session, framesize: int, dt: datetime,model:model_.Forex):
    try:
        q = db.query(model).distinct(model.id).where(model.id <= dt).order_by(
            desc(model.id)).limit(framesize).subquery('sub1')
        r = db.query(model).filter(model.id == q.c.id).order_by(model.id).all()
        return r
    except:
        pass

# Ticsデータの追加処理
def select_forex_by_id(
    db: Session,
    id: datetime,
    model:model_.Forex
) -> model_.Forex:
    return db.query(model).filter(model.id == id).first()

def add_forex(
    db: Session,
              commit: bool = True,
              schema:schema_.Forex = None,
              model:model_.Forex = None
             ) -> model_.Forex:

    exists = select_forex_by_id(
        db=db,
        id=schema.id,
        model=model
    )

#if exists is not None, data will be updated.
    if exists:
        exists.id = schema.id
        exists.close = schema.close
        exists.high = schema.high
        exists.low = schema.low
        exists.open = schema.open
        exists.volume = schema.volume
        db.commit()
        return exists
    
#if exists is None, data will be added.
    else:
        data=model(
            id=schema.id,
            close= schema.close,
            high= schema.high,
            low= schema.low,
            open= schema.open,
            volume= schema.volume,
        )
        db.add(data)
        if commit:
            db.commit()
            db.refresh(data)
        return data
        
def get_datafrom_endpoint(db: Session, models: list[model_.Forex],framesize: int ):

    date = []
    for model in models:
        last_date = get_dataframe(db=db, framesize=framesize,model=model)
        date.append(last_date[-1].id)
    return min(date)
