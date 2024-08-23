import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey

from database import Base
from hotels.models import Room


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    register_date = Column(TIMESTAMP, default=datetime.UTC)
    room_id = Column(Integer, ForeignKey("room.id"))
