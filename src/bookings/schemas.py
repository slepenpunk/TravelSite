import datetime

from pydantic import BaseModel, ConfigDict


class BookingSchema(BaseModel):
    user_id: int
    room_id: int
    date_from: datetime
    date_to: datetime
    price: int
    total_cost: int
    total_days: int

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True
    )


class BookingResponse(BaseModel):
    message: str
