from typing import List, Optional

from sqlalchemy import delete, select, update

from bookings.models import BookingModel
from bookings.service import BookingService
from database import async_session_maker
from rooms.exceptions import RoomNotFound
from rooms.models import RoomModel
from services.base import BaseService


class RoomService(BaseService):
    model = RoomModel

    @classmethod
    async def find_by_price(cls, max_price: int, min_price: int) -> List[RoomModel]:
        async with async_session_maker() as session:
            query = select(cls.model).where(
                cls.model.price.between(min_price, max_price)
            )
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def drop_room_id_of_bookings(cls, room_id: int) -> None:
        async with async_session_maker() as session:
            get_dropping_room = await BookingService.find_all(room_id=room_id)
            if get_dropping_room is None:
                raise RoomNotFound
            for room in get_dropping_room:
                drop_room_id_of_booking = (
                    update(BookingModel)
                    .where(BookingModel.id == room.id)
                    .values(room_id=None)
                )
                await session.execute(drop_room_id_of_booking)
            await session.commit()

    @classmethod
    async def delete(cls, room_id: int) -> RoomModel:
        async with async_session_maker() as session:
            get_room = await cls.find_one_or_none(id=room_id)
            if get_room is None:
                raise RoomNotFound

            await cls.drop_room_id_of_bookings(room_id=room_id)
            stmt = delete(cls.model).filter_by(id=room_id)
            await session.execute(stmt)
            await session.commit()
            return get_room
