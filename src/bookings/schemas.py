import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from bookings.exceptions import InvalidBookingDate
from rooms.exceptions import RoomNotFound


class BookingSchema(BaseModel):
    user_id: int
    price: int
    total_cost: int
    total_days: int

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True
    )


class BookingIn(BaseModel):
    room_id: int
    date_from: datetime.date
    date_to: datetime.date

    @field_validator("date_from", "date_to", mode="before")
    @classmethod
    def validate_date_format(cls, v):
        if isinstance(v, str):
            try:
                return datetime.date.fromisoformat(v)
            except ValueError:
                raise InvalidBookingDate
        return v


class BookingOut(BookingSchema):
    room_id: int
    date_from: datetime.date
    date_to: datetime.date
    id: int


class BookingResponse(BaseModel):
    message: str
