from fastapi import HTTPException
from sqlalchemy import  extract,  select, update
from . import models , schema
from sqlalchemy.orm import Session
from .dependencies  import hashed_password



async def create_account(db:Session, user:schema.UserCreate):
    username = user.username
    password = user.password
    email= user.email
    new_user = models.User(username=username,email=email, password=hashed_password(password))
    db.add(new_user)
    print("$$$$$$$$$$$4")
    try:
        await db.commit()
        return new_user  
    except Exception as e:
        print(e)
        await db.rollback()
        raise HTTPException(status_code=500, detail="User could not be added") 


        



async def login(db:Session, user:schema.UserLogin):
    username = user.username
    password = user.password 
    existing_user = await db.query(models.User).filter(models.User.username == username).first()
    if existing_user:
        if hashed_password(password) == user.password:
             return existing_user 
    return False

    

async def add_song(db:Session, song:schema.SongCreate, user_id:int):
    new_song = models.Songs(**song.dict(), user_id=user_id)
    db.add(new_song)
    try:
        await db.commit()
        await db.refresh(new_song)
        return new_song
    except Exception as e:
        print(e)
        await db.rollback()
        raise HTTPException(status_code=500, detail="song could not be added") 




async def get_song(db:Session, song_id:int):
    statement = select(models.Songs).filter(models.Songs.id == song.id)
    result = await db.execute(statement)
    song = result.fetchone()
    if not song:
        return []
    return song 




async def create_bucket(db:Session, bucket:schema.BucketCreate):
    new_bucket = models.Bucket(**bucket.dict())
    db.add(new_bucket)
    try:
        await db.commit()
        await db.refresh(new_bucket)
        return new_bucket
    except Exception as e:
        print(e)
        await db.rollback()
        raise HTTPException(status_code=500, detail="bucket could not be added") 





async def edit_profile(db:Session, profile:schema.Profile, user_id:int):
    statement = (update(models.Profile).where(models.Profile.owner_id == user_id).values(**profile.dict()).returning(models.Profile))
    try:
        result = await db.execute(statement)
        profile = await result.fetchone() 
        return profile
    except Exception as e:
        print(e)
        await db.rollback()
        raise HTTPException(status_code=500, detail="song could not be added") 





async def get_bucket_by_name(db:Session, bucket_name:str):
    statement = select(models.Bucket).filter(models.Bucket.name == bucket_name)
    result = await db.execute(statement)
    bucket = await result.fetchone()
    if not bucket:
        return []
    return bucket 




async def get_bucket_by_month(db:Session, bucket_month:str):
    statement = select(models.Bucket).filter(extract("month", models.Bucket.created_at) == bucket_month)
    result = await db.execute(statement)
    bucket = await result.fetchone()
    if not bucket:
        return []
    return bucket 




async def get_user(db:Session, user_id:int):
    statement = select(models.User).filter(models.User.id == user_id)
    result = await db.execute(statement)
    user = await result.fetchone()
    if not user:
        return []
    return user 



async def get_user_with_username(db:Session, username:str):
    statement = select(models.User).filter(models.User.username == username)
    result = await db.execute(statement)
    user = result.fetchone()
    if not user:
        return []
    return user





