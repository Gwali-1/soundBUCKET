from fastapi import FastAPI, HTTPException, Depends 
from . import db_actions, schema
from .routers import users

app = FastAPI()
app.include_router(users.router)



@app.get("/")
def home():
    return "home"


