from typing import Annotated
from fastapi import APIRouter, Cookie, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from .utility import get_auth_object , cache_handler
from ..dependencies import get_query_token,decode_token, get_token_header
from .. import schema
router = APIRouter(
    prefix="/sportify",
    tags=["sportify"]
) 



@router.get("/callback")
async def sport_home(code:str): 
    if not code:
        data = {"message":"error, something went wrong"}
        return JSONResponse(content=data, status_code= 400) 

    data = {"code":code}
    return JSONResponse(content=data, status_code= 200) 

 



#save token rout jwt and token info 
@router.post("/add_token_info")
async def add_token(code:schema.Code, user_id:int = Depends(get_token_header)):
    auth_object = get_auth_object()
    token_info = auth_object.get_access_token(code)
    await cache_handler(user_id, token_info)
    data = {"message":"Successful Authorized"}
    return JSONResponse(content=data, status_code=200)




@router.get("/authenticate")
async def authorize_spotify(user_id:int = Depends(get_query_token)):

    #check if user has token 
    auth_object = get_auth_object()
    url = auth_object.get_authorize_url()
    print(type(url))
    return RedirectResponse(url)


#create route to export laylist 
#checks if user has token first #then checks if token code in header # if none -> authorize # in header -> save , has token -> use 
