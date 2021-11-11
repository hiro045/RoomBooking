import datetime
from fastapi import FastAPI
from pydantic import BaseModel, Field

class Booking(BaseModel):
    booking_id: int
    user_id: int
    room_id: int
    booking_num: int
    start_datetime: datetime.datetime
    end_datetime: datetime.datetime

class User(BaseModel):
    user_id: int
    user_name: str = Field(max_length=20)

class Room(BaseModel):
    room_id: int
    room_name: str = Field(max_length=10)
    capacity: int

app = FastAPI()

@app.get('/')
async def index():
    return {"message": "SUCCESS"}
