from typing import Optional

from pydantic import BaseModel


class RoomSchema(BaseModel):
    name: str
    price: int

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
