from passlib.context import CryptContext
from  datetime import timedelta, datetime
from decouple import config
from jose import JWTError, jwt
from .database import SyncSessionLocal
from fastapi import HTTPException, Header, status
from typing import Annotated


SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("TOKEN_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


#hash_context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated ="auto" )



#generate access token 
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




#sync session
def get_sync_db_session():
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()



#decode access token 
def decode_token(token):
    try:
        print(type(token))
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return int(user_id)
    except Exception as e:
        print(e)
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
        )
  



#get token from header 
def get_token_header(x_token: Annotated[str, Header()]):
    if x_token:
        print(x_token)
        decoded_token = decode_token(x_token)
        return decoded_token
  

#get token from url 
def get_query_token(token: str):
    if token:
        decoded_token = decode_token(token)
        return decoded_token
 


#authenticate token 
def auth_token(token: Annotated[str, Header()]):
    try:
        id = decode_token(token)
        if id:
            return True
    except:
        return False 




