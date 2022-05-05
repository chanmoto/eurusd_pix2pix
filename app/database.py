from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from configuration import DBConfigurations
import pdb

# This will get our configuration variables, or some fallback values. But remember that these won't work as the .env file was included for the database
engine = create_engine(
    DBConfigurations.sql_alchemy_database_url,
    encoding="utf-8",
    pool_recycle=3600,
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def start_db():
    print('Starting the database.')
    Base.metadata.create_all(engine)

    print('done')

#Base.metadata = MetaData(bind=engine, schema='version2')

# スキーマを作成する
#db = SessionLocal()
#conn = engine.connect()
#scheme = 'version2'
#if not conn.dialect.has_schema(conn, scheme):
#        engine.execute(CreateSchema(scheme))

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.rollback()
        raise
    finally:
        db.close()

@contextmanager
def get_context_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.rollback()
        raise
    finally:
        db.close()
