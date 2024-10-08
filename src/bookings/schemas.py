import datetime

from pydantic import BaseModel


class BookingSchema(BaseModel):
    id: int
    user_id: int
    room_id: int
    date_from: datetime
    date_to: datetime
    price: int
    total_cost: int
    total_days: int

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
