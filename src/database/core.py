from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

DB_URL =  os.getenv("DB_URL")
print(DB_URL)
engine = create_engine(url= DB_URL, pool_pre_ping=True,
    pool_recycle=1800)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    '''
    get database session
    '''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
