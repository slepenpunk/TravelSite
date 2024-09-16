from fastapi import APIRouter

from rooms.schemas import RoomSchema
from rooms.service import RoomService

room_router = APIRouter(prefix="/rooms", tags=["Rooms"])


@room_router.get("/get-rooms")
async def get_rooms() -> list[RoomSchema]:
    return await RoomService.find_all()


@room_router.get("/get-rooms-by-id/{room_id}")
async def get_rooms_by_id(room_id: int):
    return await RoomService.find_by_id(room_id)
