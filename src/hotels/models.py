from sqlalchemy import Column, Integer, String, JSON, ForeignKey

from database import Base


class Hotel(Base):
    __tablename__ = "hotel"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    rate = Column(Integer)


class Room(Base):
    __tablename__ = "room"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer)
    privileges = Column(JSON)
