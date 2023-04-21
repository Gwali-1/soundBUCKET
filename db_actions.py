from fastapi import HTTPException
from sqlalchemy import  extract,  select, update
from . import models , schema
from sqlalchemy.orm import Session
from .dependencies  import hashed_password, verify_password



def create_account(db:Session, user:schema.UserCreate):
    username = user.username
    password = user.password
    email= user.email
    new_user = models.User(username=username,email=email, password=hashed_password(password))
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
        return new_user  
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=500, detail="User could not be added") 


        



def login(db:Session, user:schema.UserLogin):
    username = user.username
    password = user.password 
    existing_user =  db.query(models.User).filter(models.User.username == username).first()
    print(existing_user)
    if existing_user:
        print(password)
        print(existing_user.password)
        print(hashed_password(password))
        if verify_password(password, existing_user.password):
             return existing_user 
    return False

    

def add_song(db:Session, song:schema.SongCreate, user_id:int):
    new_song = models.Songs(**song.dict(), user_id=user_id)
    db.add(new_song)
    try:
        db.commit()
        db.refresh(new_song)
        return new_song
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=500, detail="song could not be added") 




def get_song(db:Session, song_id:int):
    song = db.query(models.Songs).filter(models.Songs.id == song_id).first()
    if not song:
        return []
    return song 




def create_bucket(db:Session, bucket:schema.BucketCreate):
    new_bucket = models.Bucket(**bucket.dict())
    db.add(new_bucket)
    try:
        db.commit()
        db.refresh(new_bucket)
        return new_bucket
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=500, detail="bucket could not be added") 





def edit_profile(db:Session, profile:schema.Profile, user_id:int):
    try:
        profile = db.query(models.Profile).filter(models.Profile.owner_id == user_id).update(profile.dict())
        db.commit()

        updated_profile = db.query(models.Profile).filter(models.Profile.owner_id == user_id).first()
        return updated_profile 
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=500, detail="song could not be added") 



def get_bucket_by_name(db:Session, bucket_name:str):
    bucket = db.query(models.Bucket).filter(models.Bucket.name == bucket_name).first()
    if not bucket:
        return []
    return bucket 




def get_bucket_by_month(db:Session, bucket_month:int):
    print(bucket_month)
    bucket = db.query(models.Bucket).filter(extract("month", models.Bucket.created_at) == bucket_month).first()
    if not bucket:
        return []
    return bucket




def get_user(db:Session, user_id:int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    print(user)
    if not user:
        return []
    return user 



def get_user_with_username(db:Session, username:str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return []
    return user





