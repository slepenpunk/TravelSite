from sqlalchemy import delete, update

from database import async_session_maker
from hotels.exceptions import *
from hotels.models import HotelModel
from rooms.models import RoomModel
from rooms.service import RoomService
from services.base import BaseService


class HotelService(BaseService):
    model = HotelModel

    @classmethod
    async def drop_hotel_id_of_rooms(cls, hotel_id: int) -> None:
        async with async_session_maker() as session:
            dropping_rooms = await RoomService.find_all(hotel_id=hotel_id)
            if dropping_rooms:
                for room in dropping_rooms:
                    drop_hotel_id_of_room = (
                        update(RoomModel)
                        .where(RoomModel.id == room.id)
                        .values(hotel_id=None)
                    )
                    await session.execute(drop_hotel_id_of_room)
                await session.commit()

    @classmethod
    async def delete(cls, hotel_id: int):
        get_hotel = await cls.find_one_or_none(id=hotel_id)
        if get_hotel is None:
            raise HotelNotFound

        await cls.drop_hotel_id_of_rooms(hotel_id=hotel_id)
        async with async_session_maker() as session:
            stmt = delete(cls.model).filter_by(id=hotel_id)
            await session.execute(stmt)
            await session.commit()
            return get_hotel
