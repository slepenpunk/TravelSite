from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class RoomModel(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    hotel_id = Column(ForeignKey("hotels.id"))

    hotel = relationship("HotelModel", back_populates="room")
    booking = relationship("BookingModel", back_populates="room")

    def __str__(self):
        return f"{self.name}"
