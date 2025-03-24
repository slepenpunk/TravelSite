from fastapi import APIRouter
from fastapi_cache.decorator import cache

from hotels.exceptions import HotelNotFound
from hotels.schemas import HotelSchema, HotelResponse
from hotels.service import HotelService
from rooms.exceptions import RoomNotFound
from rooms.schemas import RoomSchema
from rooms.service import RoomService

hotel_router = APIRouter(prefix="/hotels", tags=["Hotels"])


@hotel_router.get("", response_model=list[HotelSchema])
@cache(expire=30)
async def get_hotels():
    hotels = await HotelService.find_all()
    if not hotels:
        raise HotelNotFound
    return hotels


@hotel_router.get("/{city}", response_model=list[HotelSchema])
@cache(expire=30)
async def get_hotels_by_city(city: str):
    hotels = await HotelService.find_all(city=city)
    if not hotels:
        raise HotelNotFound

    return hotels


@hotel_router.get("/{name}/rooms", response_model=list[RoomSchema])
@cache(expire=30)
async def get_rooms_of_hotel(name: str):
    hotel = await HotelService.find_one_or_none(name=name)
    if hotel:
        get_rooms = await RoomService.find_all(hotel_id=hotel.id)
        if not get_rooms:
            raise RoomNotFound
    else:
        raise HotelNotFound

    rooms = [
        RoomSchema(
            name=room.name,
            price=room.price,
            hotel_name=hotel.name,
            hotel_city=hotel.city
        ) for room in get_rooms
    ]

    return rooms


@hotel_router.delete("/delete/{hotel_id}", response_model=HotelResponse)
async def delete(hotel_id: int):
    hotel = await HotelService.delete(hotel_id)
    return HotelResponse(message=f"{hotel.name} was deleted!")
