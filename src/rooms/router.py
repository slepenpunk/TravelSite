from typing import List, Any

from fastapi import APIRouter

from hotels.exceptions import HotelNotFound
from hotels.service import HotelService
from rooms.exceptions import RoomNotFound
from rooms.schemas import RoomSchema, RoomResponse
from rooms.service import RoomService

room_router = APIRouter(prefix="/rooms", tags=["Rooms"])


async def get_rooms_with_hotel_info(rooms):
    rooms_with_info = []

    for room in rooms:
        hotel = await HotelService.find_one_or_none(id=room.hotel_id)

        rooms_with_info.append(
            RoomSchema(
                name=room.name,
                price=room.price,
                hotel_name=hotel.name,
                hotel_city=hotel.city
            )
        )

    return rooms_with_info


@room_router.get("", response_model=list[RoomSchema])
async def get_all_rooms():
    get_rooms = await RoomService.find_all()
    if not get_rooms:
        raise RoomNotFound

    rooms = await get_rooms_with_hotel_info(get_rooms)
    return rooms


@room_router.get("/price/{price}", response_model=list[RoomSchema])
async def get_rooms_by_price(max_price: int, min_price: int = 0):
    get_rooms = await RoomService.find_by_price(max_price, min_price)
    if not get_rooms:
        raise RoomNotFound

    rooms = await get_rooms_with_hotel_info(get_rooms)
    return rooms


@room_router.delete("/delete/{room_id}", response_model=RoomResponse)
async def delete(room_id: int):
    room = await RoomService.delete(room_id=room_id)
    return RoomResponse(message=f"{room.name} was deleted!")
