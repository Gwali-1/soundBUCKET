from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from  decouple import config


print(config("SQL_DATABASE_URL"))

