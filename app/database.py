from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root@localhost/test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
metadata = MetaData()

database = Database(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()