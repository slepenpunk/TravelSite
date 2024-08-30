from sqlalchemy import Column, Integer, ForeignKey

from database import Base


class Booking(Base):
    __tablename__ = "booking"

    id = Column(Integer, primary_key=True)
