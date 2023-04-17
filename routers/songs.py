from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import  get_db_session,get_query_token,get_token_header
from .. import schema, db_actions
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/songs",
    tags=["Songs"]
)




#add add song to bucket
@router.post("/add_to_bucket", response_model=schema.Song)
async def add_to_bucket(song:schema.SongCreate, db:Session = Depends(get_db_session), 
                        user_id:int = Depends(get_token_header)):
    new_song = await db_actions.add_song(db, song, user_id)
    if not new_song:
        raise HTTPException(status_code=400, detail="could not create bucket")
    return new_song
    


#add song details
@router.get("song/{song_id}", response_model=schema.Song)
async def get_song(song_id:int, db:Session = Depends(get_db_session),
                   _:int = Depends(get_query_token)):
    song = await db_actions.get_song(db, song_id)
    if not song:
        return []
    return song




