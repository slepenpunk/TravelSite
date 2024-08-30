import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey

from database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    register_date = Column(TIMESTAMP, default=datetime.UTC)

