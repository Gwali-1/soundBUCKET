from typing import List
from pydantic import BaseModel
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str




############################ profile models 
class ProfileBase(BaseModel):
    sportify_profile: str | None = None
    twitter_profile: str | None = None
    profile_pic: str | None = None
    bio: str | None = None


class Profile(ProfileBase):
    contributions: int
    playlist_exports: int
    created_buckets: int
    date_joined: datetime


class ProfileCreate(ProfileBase):
    pass 



####################### song models 
class SongBase(BaseModel):
    title: str 
    song_id: str
    artist_name: str
    cover_art_url: str
    preview_url: str
    external_url: str
    song_duration: str 


class Song(SongBase):
    id: int

    class Config:
        orm_mode=True 



class SongCreate(SongBase):
    bucket_name: str 



############################# bucket models
class BucketBase(BaseModel):
    name: str
    description: str
    cover_art_url: str
 

class Bucket(BucketBase):
    id: int
    number_of_tracks: int
    upvotes: int
    songs: list[Song]

    class Config:
        orm_mode=True


class BucketCreate(BucketBase):
    pass



####################### user models
class UserBase(BaseModel):
    username: str 
    email: str 
    

class User(UserBase):
    id: int
    profile: list[Profile]  = [] 
    songs: list[Song]   = []
    
    class Config:
        orm_mode=True


class UserSongs(BaseModel):
    songs: List[Song]


class UserCreate(UserBase):
    password: str 


class UserLogin(BaseModel):
    username: str
    password: str



class Code(BaseModel):
    code: str 

