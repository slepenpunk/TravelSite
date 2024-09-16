from typing import Optional

from pydantic import BaseModel


class RoomSchema(BaseModel):
    id: int
    name: str
    price: int

    class Config:
        from_attributes = True
