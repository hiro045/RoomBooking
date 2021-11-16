from typing import List
from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

# read
@app.get('/booking', response_model=List[schemas.Booking])
async def read_booking(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    bookings = crud.get_bookings(db, skip=skip, limit=limit)
    return bookings

@app.get('/user', response_model=List[schemas.User])
async def read_user(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get('/room', response_model=List[schemas.Room])
async def read_room(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    rooms = crud.get_rooms(db, skip=skip, limit=limit)
    return rooms

# create 
@app.post('/user', response_model=schemas.User)
async def read_user(user: schemas.User, db: Session = Depends(get_db)):
    return crud.crete_user(db=db, user=user)

@app.post('/room', response_model=schemas.Room)
async def read_room(room: schemas.Room, db: Session = Depends(get_db)):
    return crud.crete_room(db=db, room=room)

@app.post('/booking', response_model=schemas.Booking)
async def read_booking(booking: schemas.Booking, db: Session = Depends(get_db)):
    return crud.crete_booking(db=db, booking=booking)
