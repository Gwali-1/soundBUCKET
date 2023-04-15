from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_db_session, create_access_token
from .. import schema, db_actions, models
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta


router = APIRouter(
    prefix="/user",
    tags=["users"]
)

ACCESS_TOKEN_EXPIRE_MINUTES=30

@router.post("/create", response_model=schema.User)
async def create_user_account(user: schema.UserCreate, db: Session = Depends(get_db_session)):
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with username already exist")
 
    new_user = await db_actions.create_account(db, user)
    if new_user:
        return new_user
    raise HTTPException(status_code=500, detail="user could not be created at the moment")




@router.post("/login", response_model=schema.Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:Session=Depends(get_db_session)):
   
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
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/authenticate_token"):
    pass 

