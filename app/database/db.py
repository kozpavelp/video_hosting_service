from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_URL = ""
engine =
session =
base = declarative_base()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close