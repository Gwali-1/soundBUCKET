from fastapi import APIRouter, Depends, HTTPException 
from fastapi.responses import RedirectResponse, JSONResponse
from .utility import get_auth_object , cache_handler
from ..dependencies import get_token_header
from .. import schema
router = APIRouter(
    prefix="/sportify",
    tags=["sportify"]
) 


#collect auth code and return it 
@router.get("/callback")
def sport_home(code:str): 
    if not code:
        data = {"message":"error, something went wrong"}
        return JSONResponse(content=data, status_code= 400) 

    data = {"code":code}
    return JSONResponse(content=data, status_code= 200) 

 


#get token info and save 
@router.post("/add_token_info")
def add_token(code:schema.Code, user_id:int = Depends(get_token_header)):
    auth_object = get_auth_object()
    token_info = auth_object.get_access_token(code)
    if token_info:
        try:
            cache_handler(user_id, token_info)
            data = {"message":"Successful Authorized"}
            return JSONResponse(content=data, status_code=200)

        except:
            raise HTTPException(status_code=401, detail="could not authorize at the moment")

    raise HTTPException(status_code=401, detail="could not authorize at the moment")



#spotofy auth route 
@router.get("/authenticate")
def authorize_spotify():
    #check if user has token 
    auth_object = get_auth_object()
    url = auth_object.get_authorize_url()
    return RedirectResponse(url)


