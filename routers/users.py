from fastapi import APIRouter, Depends, HTTPException, Response, responses
from ..dependencies import  get_db_session, create_access_token,auth_token, get_query_token
from .. import schema, db_actions
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from fastapi.responses import JSONResponse



router = APIRouter(
    prefix="/user",
    tags=["users"]
)


ACCESS_TOKEN_EXPIRE_MINUTES=30




@router.post("/create", response_model=schema.User)
async def create_user_account(user: schema.UserCreate, db: Session = Depends(get_db_session)):
    existing_user = await db_actions.get_user_with_username(db, user.username) 
    if existing_user:
        raise HTTPException(status_code=400, detail="User with username already exist")
    new_user = await db_actions.create_account(db, user)
    print(new_user)
    if new_user:
        print(new_user)
        return new_user

    print("no")
    raise HTTPException(status_code=500, detail="user could not be created at the moment")






@router.post("/login", response_model=schema.Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],response:Response, db:Session=Depends(get_db_session)):
   
    data = {
        "username": form_data.username,
        "passeord": form_data.password
    } 

    login_credentials =schema.UserLogin(**data)

    user = await db_actions.login(db,login_credentials) 
    if not user:
        raise HTTPException(
            status_code=401, 
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    response.set_cookie(key="user_id", value=access_token)
    return {"access_token": access_token, "token_type": "bearer"}






@router.post("/authenticate_token")
async def authenticate_token(check:bool = Depends(auth_token)):
    if check:
        return JSONResponse(content={"message":"valid"},status_code=200)
    return JSONResponse(content={"message":"invalid"},status_code=401)




@router.get("/user", response_model=schema.User)
async def get_user(id: int = Depends(get_query_token), db:Session=Depends(get_db_session)):
    user = await db_actions.get_user(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user




@router.get("/user/songs", response_model=schema.UserSongs)
async def get_user_song(db:Session = Depends(get_db_session), user_id:int = Depends(get_query_token)):
    user = await db_actions.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")   
    return user.songs


