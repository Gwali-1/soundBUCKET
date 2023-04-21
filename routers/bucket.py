from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import  get_sync_db_session,get_query_token,get_token_header
from .. import schema, db_actions
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/bucket",
    tags=["Bucket"],
)


@router.post("/create_bucket", response_model=schema.Bucket)
def make_bucket(bucket:schema.BucketCreate, db:Session = Depends(get_sync_db_session),
                        _:int = Depends(get_token_header)):
    new_bucket = db_actions.create_bucket(db, bucket)
    if not new_bucket:
        raise HTTPException(status_code=400, detail="could not create bucket")
    return new_bucket 




@router.get("/get_bucket_by_name", response_model=schema.Bucket)
def get_bucket_with_name(bucket_name:str, db:Session = Depends(get_sync_db_session),
                        _:int = Depends(get_query_token)):
    bucket = db_actions.get_bucket_by_name(db, bucket_name)
    if not bucket:
        raise HTTPException(status_code=400, detail="Bucket not found")
    return bucket




@router.get("/get_bucket_by_month", response_model=schema.Bucket)
def get_bucket_with_month(bucket_month:int, db:Session = Depends(get_sync_db_session),
                        _:int = Depends(get_query_token)):
    bucket = db_actions.get_bucket_by_month(db, bucket_month)
    if not bucket:
        raise HTTPException(status_code=400, detail="Bucket not found")
    return bucket





@router.get("/all_buckets")
def get_buckets(db:Session = Depends(get_sync_db_session),_:int= Depends(get_query_token)):
    buckets = db_actions.get_all_buckets(db)
    if not buckets:
        raise HTTPException(status_code=404, detail="no buckets found")
    return buckets














