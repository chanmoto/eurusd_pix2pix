from sqlalchemy import Column, Integer, Float, DateTime
from database import Base

class Forex():
    __tablename__ = "forex"
    id = Column(DateTime(timezone=True), primary_key=True,
                index=True, unique=True,)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)

class Forex_short(Forex, Base):
    __tablename__ = "forex_short"

class Forex_middle(Forex,Base):
    __tablename__ = "forex_middle"

class Forex_long(Forex,Base):
    __tablename__ = "forex_long"