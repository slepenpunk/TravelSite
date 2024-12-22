from pydantic import BaseModel


class RoomSchema(BaseModel):
    name: str
    price: int
    hotel_name: str
    hotel_city: str

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class RoomResponse(BaseModel):
    message: str
