from fastapi import APIRouter

from hotels.service import HotelService
from rooms.service import RoomService

hotel_router = APIRouter(prefix="/hotels", tags=["Hotels"])


@hotel_router.get("")
async def get_hotels():
    return await HotelService.find_all()


@hotel_router.get("/{location}")
async def get_hotels_by_location(location: str):
    return await HotelService.find_all(location=location)


@hotel_router.get("/{hotel_id}/rooms")
async def get_rooms_of_hotel(hotel_id: int):
    return await RoomService.find_all(hotel_id=hotel_id)


@hotel_router.delete("/delete/{hotel_id}")
async def delete(hotel_id: int):
    hotel = await HotelService.delete(hotel_id)
    return {"message": f"{hotel.name} was deleted!"}
