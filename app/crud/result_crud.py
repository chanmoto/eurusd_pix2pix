from datetime import datetime
from typing import List

from models.result_model import ResultBase as model
from schemas.result_schema import Result as schema
from sqlalchemy.orm import Session


def select_all(db: Session) -> List[schema]:
    return db.query(model).all()

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
        exists.realA = obj.realA
        exists.realB = obj.realB
        exists.fakeB = obj.fakeB
        exists.signal = obj.signal
        db.commit()
        return exists
    
#if exists is None, data will be added.
    else:
        data=model(
            id=obj.id,
            realA= obj.realA,
            realB= obj.realB,
            fakeB= obj.fakeB,
            signal= obj.signal,
        )
        db.add(data)
        db.commit()
        db.refresh(data)
        return data

"""
def update_experiment_artifact_file_paths(
    db: Session,
    experiment_id: str,
    artifact_file_paths: Dict,
) -> schemas.Experiment:
    data = select_experiment_by_id(
        db=db,
        experiment_id=experiment_id,
    )
    if data.artifact_file_paths is None:
        data.artifact_file_paths = artifact_file_paths
    else:
        for k, v in artifact_file_paths.items():
            data.artifact_file_paths[k] = v
    db.commit()
    db.refresh(data)
    return data
"""
