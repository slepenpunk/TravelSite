from sqlalchemy import Column, Integer, String, JSON

from database import Base


class HotelModel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    rate = Column(Integer)



