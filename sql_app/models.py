from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from .database import Base

class User(Base):
    __tablename__ = 'tb_user'
    user_id = Column(Integer, primary_key=True, index=True)
    user_nane = Column(String, unique=True, index=True)

class Room(Base):
    __tablename__ = 'tb_room'
    room_id = Column(Integer, primary_key=True, index=True)
    room_name = Column(String, unique=True, index=True)
    capacity = Column(Integer)

class Booking(Base):
    __tablename__ = 'tb_booking'
    booking_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('tb_user.user_id'), ondelete='SET NULL', nullable=True)
    room_id = Column(Integer, ForeignKey('tb_room.room_id'), ondelete='SET NULL', nullable=True)
    booking_num = Column(Integer)
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)