from fastapi import APIRouter

from rooms.exceptions import RoomIsNotFound
from rooms.service import RoomService

room_router = APIRouter(prefix="/rooms", tags=["Rooms"])


@room_router.get("")
async def get_rooms():
    return await RoomService.find_all()


@room_router.get("/{room_id}")
async def get_room_by_id(room_id: int):
    return await RoomService.find_by_id(room_id)


@room_router.get("/price/{price}")
async def get_rooms_by_price(max_price: int, min_price: int = 0):
    return await RoomService.find_by_price(max_price, min_price)


@room_router.delete("/delete/{room_id}")
async def delete(room_id: int):
    room = await RoomService.delete(id=room_id)
    if not room:
        raise RoomIsNotFound
    return {"message": f"{room.name} was deleted!"}
