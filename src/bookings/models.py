from sqlalchemy import Column, Computed, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship

from database import Base


class BookingModel(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id"))
    room_id = Column(ForeignKey("rooms.id"))
    date_from = Column(Date, nullable=False)
    date_to = Column(Date, nullable=False)
    price = Column(Integer, nullable=False)
    total_cost = Column(Integer, Computed("(date_to - date_from) * price"))
    total_days = Column(Integer, Computed("date_to - date_from"))

    user = relationship("UserModel", back_populates="booking")
    room = relationship("RoomModel", back_populates="booking")

    def __str__(self):
        return f"Booking #{self.id}"
