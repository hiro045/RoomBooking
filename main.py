import datetime
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

@app.get('/')
async def index():
    return {"message": "SUCCESS"}

@app.post('/booking')
async def create_booking(booking: Booking):
    return {"booking": booking}

@app.post('/user')
async def create_user(user: User):
    return {"user": user}

@app.post('/room')
async def create_room(room: Room):
    return {"room": room}
