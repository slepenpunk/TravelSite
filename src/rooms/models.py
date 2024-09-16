from sqlalchemy import Column, Integer, String, JSON
from database import Base


class RoomModel(Base):
    __tablename__ = "room"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer)


