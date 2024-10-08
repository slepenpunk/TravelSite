from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from database import Base


class RoomModel(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    hotel_id = Column(ForeignKey("hotels.id"))


