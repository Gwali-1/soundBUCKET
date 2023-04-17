from passlib.context import CryptContext
from  datetime import timedelta, datetime
from decouple import config
from jose import JWTError, jwt
from .async_database import SessionLocal
from fastapi import HTTPException, Header, status
from typing import Annotated


SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("TOKEN_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated ="auto" )




def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def hashed_password(password: str):
    return pwd_context.hash(password)



###dependecies
async def get_db_session():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()





async def decode_token(token):
    try:
        payload = jwt.decode(token,SECRET_KEY, ALGORITHM)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_id
    except JWTError:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
        )
  




async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token:
        decoded_token = await decode_token(x_token)
        return decoded_token
  





async def get_query_token(token: str):
    if token:
        decoded_token = await decode_token(token)
        return decoded_token
 





async def auth_token(token: Annotated[str, Header()]):
    try:
        id = await decode_token(token)
        if id:
            return True
    except:
        return False 

