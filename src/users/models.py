import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

    booking = relationship("BookingModel", back_populates="user")

    def __str__(self):
        return f"User {self.email}"
