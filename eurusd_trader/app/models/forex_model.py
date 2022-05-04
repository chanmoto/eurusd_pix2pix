from sqlalchemy import Column, Integer, Float, DateTime,func
from database import Base
from sqlalchemy.orm import Session
from sqlalchemy_utils import get_class_by_table
from sqlalchemy import desc
from datetime import datetime

class Forex():
    __tablename__ = "forex"
    id = Column(DateTime(timezone=True), primary_key=True,
                index=True, unique=True,)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)

class Forex2_m5(Forex, Base):
    __tablename__ = "forex2_m5"

class Forex2_m30(Forex,Base):
    __tablename__ = "forex2_m30"

class Forex2_m240(Forex,Base):
    __tablename__ = "forex2_m240"