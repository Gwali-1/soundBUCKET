from typing import Annotated
from fastapi import APIRouter, Cookie, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from .utility import get_auth_object , cache_handler
from ..dependencies import get_query_token,decode_token
router = APIRouter(
    prefix="/sportify",
    tags=["sportify"]
) 



@router.get("/callback")
async def sport_home(code:str, user_id: Annotated[str|None, Cookie()]):
    auth_object = get_auth_object()
    token_info = auth_object.get_access_token(code)
    #save token to db 
    #make sure to set Cookie user_id 
    decoded_id = decode_token(user_id)
    await cache_handler(decoded_id, token_info)

    return token_info




@router.get("/authenticate")
async def authorize_spotify(user_id:int = Depends(get_query_token)):

    #check if user has token 
    auth_object = get_auth_object()
    url = auth_object.get_authorize_url()
    print(type(url))
    return RedirectResponse(url)



