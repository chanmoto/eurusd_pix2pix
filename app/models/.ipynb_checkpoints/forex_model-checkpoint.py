from sqlalchemy import Column, Integer, Float, DateTime,func
from database import Base
from sqlalchemy.orm import Session
from sqlalchemy_utils import get_class_by_table
from sqlalchemy import desc
from datetime import datetime

class forexbase():
    __tablename__ = "forex"
    id = Column(DateTime(timezone=True), primary_key=True,
                index=True, unique=True,)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)

    def __init__(self):
        self.id = None
        pass

    def select_forex_by_name(self, db: Session, table_name: str)-> object:
        return get_class_by_table(
            Base, Base.metadata.tables.get(table_name)
        )

    def get_last_time(self,db: Session):
        try:
            model = self.select_forex_by_name(
                db=db, table_name=self.__tablename__)
            q = db.query(func.max(model.id).label('id_max')).subquery('sub1')
            r = db.query(model).filter(model.id == q.c.id_max).all()

            return str(r[0].id).replace("-", ".")
        except:
            pass

    def get_dataframe(self,db:Session,framesize: int):
        model = self.select_forex_by_name(
                db=db, table_name=self.__tablename__)
        try:
            q = db.query(model).distinct(model.id).order_by(desc(model.id)).limit(framesize).subquery('sub1')
            r = db.query(model).filter(model.id == q.c.id ).order_by(model.id).all()
            return r
        except:
            pass

    def get_dataframe_all(self,db:Session):
        model = self.select_forex_by_name(
                db=db, table_name=self.__tablename__)
        try:
            q = db.query(model).distinct(model.id).order_by(desc(model.id)).all()
            return q
        except:
            pass


    def get_dataframe_span(self, db: Session, framesize: int, dt : datetime):
        df = self.select_forex_by_name(
                db=db,table_name=self.__tablename__)
        try:
            q = db.query(df).distinct(df.id).where(df.id <= dt).order_by(desc(df.id)).limit(framesize).subquery('sub1')
            r = db.query(df).filter(df.id == q.c.id ).order_by(df.id).all()
            return r
        except:
            pass

#Ticsデータの追加処理
    def add_forex(self,
        db: Session,
        time: datetime,
        value: dict = None,
        commit: bool = True,):

        self.id=time
        self.close=value.close
        self.high=value.high
        self.low=value.low
        self.open=value.open
        self.volume=value.volume
        
        db.add(self)
        if commit:
            db.commit()
            db.refresh(self)
        return self

class forex2_m5(forexbase, Base):
    __tablename__ = "forex2_m5"

class forex2_m30(forexbase,Base):
    __tablename__ = "forex2_m30"

class forex2_m240(forexbase,Base):
    __tablename__ = "forex2_m240"