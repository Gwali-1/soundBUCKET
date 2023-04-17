from fastapi import FastAPI, HTTPException, Depends 
from . import db_actions, schema
from .routers import users, bucket, songs

app = FastAPI()
app.include_router(users.router)
app.include_router(bucket.router)
app.include_router(songs.router)


@app.get("/")
def home():
    return "home"


