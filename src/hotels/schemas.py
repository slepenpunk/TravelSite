from pydantic import BaseModel


class HotelSchema(BaseModel):
    name: str
    rate: int
    city: str
    address: str


class HotelResponse(BaseModel):
    message: str
