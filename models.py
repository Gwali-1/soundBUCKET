import async_database
from sqlalchemy import ForeignKeyConstraint, String, Integer, Boolean, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

Base = async_database.Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String, index=True)
    password = Column(String)
    profile = relationship("Profile")
    songs = relationship("Songs")


class Profile(Base):
    __tablename__ = "profile"
    id = Column(Integer, primary_key=True, index=True)
    contributions = Column(Integer, default=0)
    playlist_exports = Column(Integer, default=0)
    music_taste_upvote = Column(Integer, default=0)
    sportify_profile = Column(String)
    twitter_profile = Column(String)
    profile_pic = Column(String)
    bio = Column(String)
    date_joined = Column(DateTime)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)


    

class Songs(Base):
    __tablename__ = "songs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    song_id = Column(String, index=True)
    artist_name = Column(String)
    cover_art_url = Column(String)
    preview_url = Column(String)
    song_duration = Column(String)
    external_url = Column(String)
    added_at = Column(DateTime, index=True, default=datetime.now)
    user_id = Column(Integer, ForeignKey("users.id"))
    bucket_id = Column(Integer, ForeignKey("bucket.id"))

    



class Bucket(Base):
    __tablename__ = "bucket"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True , index=True)
    description = Column(String)
    number_of_tracks = Column(Integer)
    created_at = Column(DateTime,index=True, default=datetime.now)
    cover_art_url = Column(String)
    upvotes = Column(Integer, default=0)
    songs = relationship("Songs")
    


 










