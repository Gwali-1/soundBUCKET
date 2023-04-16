from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import  get_db_session,get_query_token,get_token_header
from .. import schema, db_actions, models
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.responses import JSONResponse


router = APIRouter(
    prefix="/bucket",
    tags=["Bucket"],
)


#add create bucket
@router.post("/create_bucket", response_model=schema.Bucket)
async def create_bucket(bucket:schema.Bucket, db:Session = Depends(get_db_session),
                        _:int = Depends(get_token_header)):
    new_bucket = await db_actions.create_bucket(db, bucket)
    if not new_bucket:
        raise HTTPException(status_code=400, detail="could not create bucket")
    return new_bucket


        


#add get bucket songs with bucket name


#add get bucket songs with bucket month

