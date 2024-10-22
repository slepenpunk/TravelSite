from fastapi import APIRouter

from rooms.exceptions import RoomIsNotFound
from rooms.service import RoomService

room_router = APIRouter(prefix="/rooms", tags=["Rooms"])


@room_router.get("/hotel/{hotel_id}")
async def get_rooms_of_hotel(hotel_id: int):
    return await RoomService.find_all(hotel_id=hotel_id)


@room_router.get("/{room_id}")
async def get_rooms_by_id(room_id: int):
    return await RoomService.find_by_id(room_id)


@room_router.delete("")
async def delete(room_id: int):
    get_room = await RoomService.delete_by_id(room_id)
    if not get_room:
        raise RoomIsNotFound
    return {"message": f"{get_room.name} was deleted!"}
