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
    realA = Column(
        pg.ARRAY(Float),
        comment="realA"
    )
    realB = Column(
        pg.ARRAY(Float),
        comment="realB"
    )
    fakeB = Column(
        pg.ARRAY(Float),
        comment="fakeB"
    )
    signal = Column(
        Float,
        comment="signal"
    )
