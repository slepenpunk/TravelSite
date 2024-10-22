from fastapi import APIRouter

from hotels.exceptions import HotelNotFound
from hotels.service import HotelService

hotel_router = APIRouter(prefix="/hotels", tags=["Hotels"])


@hotel_router.get("")
async def get_hotels():
    return await HotelService.find_all()


@hotel_router.delete("/delete")
async def delete(hotel_id: int):
    get_hotel = await HotelService.delete_by_id(hotel_id)
    if not get_hotel:
        raise HotelNotFound
    return {"message": f"{get_hotel.name} was deleted!"}
