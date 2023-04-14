from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, declarative_base
from  decouple import config

URL=  config("SQL_DATABASE_URL")
engine = create_engine(URL)
SessionLocal = sessionmaker(autocommit=False , autoflush=False , bind=engine)
Base = declarative_base()
 



