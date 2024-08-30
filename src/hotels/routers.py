from typing import List

from fastapi import APIRouter
from sqlalchemy import select, insert

from database import async_session_maker
from hotels.models import Room as RoomModel
from hotels.schemas import Room as RoomSchema

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("/get-rooms")
async def get_rooms():
    async with async_session_maker() as session:
        query = select(RoomModel)
        result = await session.execute(query)
        return result.scalars().all()


@router.post("/add-room")
async def add_room(new_room: RoomSchema):
    async with async_session_maker() as session:
        query = RoomModel(name=new_room.name,price=new_room.price,privelege=new_room.privilege)
        session.add(query)
        await session.commit()
        session.refresh(query)
        return query


