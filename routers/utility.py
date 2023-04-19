from ..async_database import SessionLocal
from .. import models 
from spotipy.oauth2 import SpotifyOAuth
import time 
from decouple import config


def get_auth_object():
    return  SpotifyOAuth(
        client_id=config("client_id"),
        client_secret=config("client_secret"),
        redirect_uri="http://localhost:8000/sportify/callback",
        scope="playlist-modify-public playlist-modify-private"

    )




async def get_token_from_db(user_id):
    #database query
    db = SessionLocal()
    user = await db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        token = user.token
        if token:
            await db.close()
            return {
                'access_token': token[0],
                'expires_at': token[2],
                'refresh_token': token[1]
            }
    return None





async def save_token_to_db(user_id, token_info):
    db = SessionLocal()
    try:
        new_token = models.Tokens(token=token_info["access_token"], expires_at=token_info["expires_at"],
                                  refresh_token=token_info["refresh_token"], owner_id=user_id)
        db.add(new_token)
        await db.commit()
    except:
        await db.rollback()
    finally:
        await db.close()




async def cache_handler(user_id, token_info = None):
    if token_info is None:
        token_data = await get_token_from_db(user_id)
        if token_data and token_data['expires_at'] > time.time():
            return token_data['access_token']
        else:
            new_token_data = await get_new_token(token_data["refresh_token"])
            await save_token_to_db(user_id, new_token_data)
            return new_token_data['access_token']

    await save_token_to_db(user_id, token_info)






def get_new_token(refresh_token):  
    sp_oauth = get_auth_object()
    token_info = sp_oauth.refresh_access_token(refresh_token)
    return {
        'access_token': token_info['access_token'],
        'expires_at': token_info['expires_at'],
        'refresh_token': token_info['refresh_token']
    }



