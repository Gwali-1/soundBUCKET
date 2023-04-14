from sqlalchemy.orm import sessionmaker, declarative_base
from  decouple import config
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

URL=  config("SQL_DATABASE_URL")
print(URL)
engine = create_async_engine(URL, echo=True,future=True)
SessionLocal = async_sessionmaker(engine, class_=AsyncSession)
Base = declarative_base()



