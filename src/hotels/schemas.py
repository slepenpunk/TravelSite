from typing import Optional, List

from pydantic import BaseModel


class Privilege(BaseModel):
    has_spa: bool
    has_mini_bar: bool


class Room(BaseModel):
    id: int
    name: str
    price: int
    privilege: Optional[Privilege] = None
