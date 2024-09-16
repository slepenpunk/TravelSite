from pydantic import BaseModel


class HotelSchema(BaseModel):
    id: int
    name: str
    rate: int
