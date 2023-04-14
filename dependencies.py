from enum import auto
from passlib.context import CryptContext
from  datetime import timedelta, datetime
from decouple import config
from jose import jwt 
from .async_database import SessionLocal


SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("TOKEN_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bycrypt"], deprecated = auto)




def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hashed_password(password):
    return pwd_context.hash(password)



###dependecies
async def get_db_session():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
