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












def get_token_from_db(user_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT access_token, expires_at, refresh_token FROM tokens WHERE user_id=?", (user_id,))
    token_data = c.fetchone()
    conn.close()
    if token_data:
        return {
            'access_token': token_data[0],
            'expires_at': token_data[1],
            'refresh_token': token_data[2]
        }
    else:
        return None

def save_token_to_db(user_id, access_token, expires_at, refresh_token):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO tokens (user_id, access_token, expires_at, refresh_token) VALUES (?, ?, ?, ?)", (user_id, access_token, expires_at, refresh_token))
    conn.commit()
    conn.close()

def cache_handler(user_id):
    token_data = get_token_from_db(user_id)
    if token_data and token_data['expires_at'] > time.time():
        return token_data['access_token']
    else:
        new_token_data = get_new_token_data_from_api()
        save_token_to_db(user_id, new_token_data['access_token'], new_token_data['expires_at'], new_token_data['refresh_token'])
        return new_token_data['access_token']





def get_new_token_data_from_api():
    sp_oauth = SpotifyOAuth(client_id='your_client_id', client_secret='your_client_secret', redirect_uri='your_redirect_uri', scope='your_scope')
    token_info = sp_oauth.get_access_token()
    return {
        'access_token': token_info['access_token'],
        'expires_at': token_info['expires_at'],
        'refresh_token': token_info['refresh_token']
    }
