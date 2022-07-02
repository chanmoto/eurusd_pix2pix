from database import Base
from sqlalchemy import Column ,Float
from sqlalchemy.sql.sqltypes import  DateTime
from sqlalchemy.dialects import postgresql as pg

class ResultBase(Base):
    __tablename__ = "result"

    id = Column(
        DateTime,
        primary_key=True,
        comment="datetime"
    )
    reala = Column(
        pg.ARRAY(Float),
        comment="reala"
    )
    realb = Column(
        pg.ARRAY(Float),
        comment="realb"
    )
    fakeb = Column(
        pg.ARRAY(Float),
        comment="fakeb"
    )
    signal = Column(
        Float,
        comment="signal"
    )
