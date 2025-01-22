from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship

from database import Base


class HotelModel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    rate = Column(Integer, nullable=False)
    city = Column(String)
    address = Column(String)

    room = relationship("RoomModel", back_populates="hotel")

    def __str__(self):
        return f"{self.name}"

