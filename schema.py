from pydantic import BaseModel
from sqlalchemy import DateTime



class ProfileBase(BaseModel):
    sportify_profile: str | None = None
    twitter_profile: str | None = None
    profile_pic: str | None = None
    bio: str | None = None



class Profile(ProfileBase):
    contributions: int
    playlist_exports: int
    created_buckets: int
    date_joined: DateTime



class ProfileCreate(ProfileBase):
    pass 



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

class SongCreate(SongBase):
    song_id: str
    artist_name
class BucketBase(BaseModel):
    pass


class UserBase(BaseModel):
    pass

class User(BaseModel):
    id: int
    username: str 
    email: str 
    profile: list[Profile]
    songs: list[Songs] 
 

class UserCreate(BaseModel):
    username: str
    email: str 
    password: str 



