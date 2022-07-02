from datetime import datetime
from typing import List

from models.result_model import ResultBase as model
from schemas.result_schema import Result as schema
from sqlalchemy.orm import Session


def select_all(db: Session, start:datetime , end : datetime) -> List[schema]:
    return db.query(model).order_by(model.id.desc()).first()


def select_by_id(
    db: Session,
    id: datetime,
) -> model:
    return db.query(model).filter(model.id == id).first()

def add(
    db: Session,
    obj: schema,
) -> model:

    exists = select_by_id(
        db=db,
        id=obj.id
    )

#if exists is not None, data will be updated.
    if exists:
        exists.id = obj.id
        exists.reala = obj.reala
        exists.realb = obj.realb
        exists.fakeb = obj.fakeb
        exists.signal = obj.signal
        db.commit()
        return exists
    
#if exists is None, data will be added.
    else:
        data=model(
            id=obj.id,
            reala= obj.reala,
            realb= obj.realb,
            fakeb= obj.fakeb,
            signal= obj.signal,
        )
        db.add(data)
        db.commit()
        db.refresh(data)
        return data

def get_result_span( db: Session, start_date:datetime,end_date:datetime ) -> List[schema]:
    return db.query(model).distinct(model.id).filter(model.id <= end_date).filter(model.id >= start_date).order_by(model.id)
    