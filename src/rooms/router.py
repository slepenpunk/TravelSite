from typing import List, Any

from fastapi import APIRouter

from rooms.exceptions import RoomNotFound
from rooms.schemas import RoomSchema
from rooms.service import RoomService

room_router = APIRouter(prefix="/rooms", tags=["Rooms"])


@room_router.get("", response_model=list[RoomSchema])
async def get_rooms():
    return await RoomService.find_all()


@room_router.get("/price/{price}", response_model=list[RoomSchema])
async def get_rooms_by_price(max_price: int, min_price: int = 0):
    query = await RoomService.find_by_price(max_price, min_price)
    if not query:
        raise RoomNotFound
    return query


@room_router.delete("/delete/{room_id}")
async def delete(room_id: int):
    room = await RoomService.delete(room_id=room_id)
    return {"message": f"{room.name} was deleted!"}
