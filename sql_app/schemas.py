import datetime
from pydantic import BaseModel, Field

class Booking(BaseModel):
    booking_id: int
    user_id: int
    room_id: int
    booking_num: int
    start_datetime: datetime.datetime
    end_datetime: datetime.datetime

    class Config:
        orm_mode = True

class User(BaseModel):
    user_id: int
    user_name: str = Field(max_length=20)
    
    class Config:
        orm_mode = True

class Room(BaseModel):
    room_id: int
    room_name: str = Field(max_length=10)
    capacity: int
    
    class Config:
        orm_mode = True