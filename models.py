from .database import Base
from sqlalchemy import ForeignKeyConstraint, String, Integer, Boolean, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship


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
    contributions = Column(Integer)
    playlist_exports = Column(Integer)
    created_buckets = Column(Integer)
    music_tatse = Column(Integer)
    sportify_profile = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))


    

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
    added_at = Column(DateTime, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    bucket_id = Column(Integer, ForeignKey("bucket.id"))

    



class Bucket(Base):
    __tablename__ = "bucket"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    nuimber_of_tracks = Column(Integer)
    created_at = Column(DateTime, index=True)
    cover_art_url = Column(String)
    songs = relationship("Songs")
    


 










