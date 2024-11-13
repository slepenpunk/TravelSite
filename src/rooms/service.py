from sqlalchemy import select

from database import async_session_maker
from rooms.models import RoomModel
from services.base import BaseService


class RoomService(BaseService):
    model = RoomModel

    @classmethod
    async def find_by_price(cls, max_price: int, min_price: int):
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.price.between(min_price, max_price))
            result = await session.execute(query)
            rooms = result.scalars().all()
            return rooms
