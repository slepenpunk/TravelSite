import logging

from fastapi import APIRouter
from fastapi_cache.decorator import cache
from sqlalchemy import text

from database import async_session_maker
from hotels.service import HotelService
from logger import handle_and_log_errors
from rooms.exceptions import RoomNotFound
from rooms.schemas import RoomSchema
from rooms.service import RoomService

room_router = APIRouter(prefix="/rooms", tags=["Rooms"])
logger = logging.getLogger(__name__)


async def get_rooms_with_hotel_info(rooms) -> list[RoomSchema]:
    rooms_with_info = []

    for room in rooms:
        hotel = await HotelService.find_one_or_none(id=room.hotel_id)

        rooms_with_info.append(
            RoomSchema(
                name=room.name,
                price=room.price,
                hotel_name=hotel.name,
                hotel_city=hotel.city,
            )
        )

    return rooms_with_info


@room_router.get("/check_db")
async def check_db():
    async with async_session_maker() as session:
        result = await session.execute(text("SELECT current_database()"))
        current_db = result.scalar()
        return {"current_database": current_db}


@room_router.get("", response_model=list[RoomSchema])
@cache(expire=30)
@handle_and_log_errors(logger=logger)
async def get_all_rooms():
    try:
        get_rooms = await RoomService.find_all()
        if not get_rooms:
            raise RoomNotFound
        rooms = await get_rooms_with_hotel_info(get_rooms)
        return rooms
    except Exception as e:
        logger.error(f"Error info: {e}", exc_info=True)
        raise


@room_router.get("/price", response_model=list[RoomSchema])
@cache(expire=30)
@handle_and_log_errors(logger=logger)
async def get_rooms_by_price(max_price: int, min_price: int = 0):
    get_rooms = await RoomService.find_by_price(max_price, min_price)
    if not get_rooms:
        raise RoomNotFound
    rooms = await get_rooms_with_hotel_info(get_rooms)
    return rooms
