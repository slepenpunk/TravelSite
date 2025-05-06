from pydantic import BaseModel, ConfigDict


class RoomSchema(BaseModel):
    name: str
    price: int
    hotel_name: str
    hotel_city: str

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class RoomResponse(BaseModel):
    message: str
