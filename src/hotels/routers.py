from typing import List

from fastapi import APIRouter

from hotels.schemas import Room

router = APIRouter(prefix="/hotels", tags=["Hotels"])

test_db = [
    {"id": 1, "name": "Standard", "price": 1000},
    {"id": 2, "name": "Deluxe", "price": 5000, "privilege": [
        {"has_spa": True, "has_mini_bar": True}

    ]}
]


@router.get("/get-room/{room_id}", response_model=List[Room])
async def get_room_by_id(room_id: int):
    return [room for room in test_db if room.get("id") == room_id]


@router.post("/add-room")
async def add_new_room(new_room: Room):
    room = {
        "id": new_room.id,
        "name": new_room.name,
        "price": new_room.price,
        "privilege": new_room.privilege
    }
    test_db.append(room)
    return (f"Room was add!"
            f"{room}")
