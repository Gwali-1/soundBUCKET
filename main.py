from fastapi import FastAPI, HTTPException, Depends
from . import db_actions, schema
from .routers import users, bucket, songs, sportify_operations
from fastapi.middleware.cors import CORSMiddleware


origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(bucket.router)
app.include_router(songs.router)
app.include_router(sportify_operations.router)


@app.get("/")
def home():
    return "home"


