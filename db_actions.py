from sqlalchemy import  extract
from . import models , schema
from sqlalchemy.orm import Session
from .dependencies  import hashed_password



async def create_account(db:Session, user:schema.UserCreate):
    username = user.username
    password = user.password
    email= user.email
    new_user = models.User(username=username,email=email, password=hash_password(password))
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
        return new_user 
    except Exception as e:
        await db.rollback()
        raise e
        



async def login(db:Session, user:schema.UserLogin):
    username = user.username
    password = user.password 
    existing_user = await db.query(models.User).filter(models.User.username == username).first()
    if existing_user:
        if hashed_password(password) == user.password:
             return existing_user 
    return False

    

async def add_song(db:Session, song:schema.SongCreate):
    new_song = models.Songs(**song.dict())
    db.add(new_song)
    try:
        await db.commit()
        await db.refresh(new_song)
        return new_song
    except Exception as e:
        print(e)
        raise e 



async def create_bucket(db:Session, bucket:schema.Bucket):
    new_bucket = models.Bucket(**bucket.dict())
    db.add(new_bucket)
    try:
        await db.commit()
        await db.refresh(new_bucket)
        return new_bucket
    except Exception as e:
        print(e)
        db.rollback()
        raise e



async def edit_profile(db:Session, profile:schema.Profile, user_id:int):
    user_profile = await db.query(models.Profile).filter(models.Profile.owner_id == user_id).update(**profile.dict())                                             
    try:
        await db.commit()
        await db.refresh(user_profile)
        return profile
    except Exception as e:
        print(e)
        db.rollback()
        raise e




async def get_bucket_songs_by_name(db:Session, bucket_name:str):
    bucket = await db.query(models.Bucket).filter(models.Bucket.name == bucket_name).first()
    if not bucket:
        return []
    return bucket 




async def get_bucket_songs_by_month(db:Session, bucket_month:str):
    bucket = await db.query(models.Bucket).filter(extract("month", models.Bucket.created_at) == bucket_month).first()
    if not bucket:
        return []
    return bucket 




async def get_user(db:Session, user_id:int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return []
    return user 
    




