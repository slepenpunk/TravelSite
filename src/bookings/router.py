import json
from datetime import date

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from pydantic import TypeAdapter

from bookings.exceptions import BookingNotFound
from bookings.schemas import BookingSchema, BookingResponse
from bookings.service import BookingService
from rooms.exceptions import RoomCannotBeBooked
from tasks.tasks import send_booking_confirmation
from users.dependencies import get_current_user
from users.models import UserModel

booking_router = APIRouter(prefix="/bookings", tags=["Bookings"])


@booking_router.get("", response_model=list[BookingSchema])
@cache(expire=30)
async def get_bookings(user: UserModel = Depends(get_current_user)):
    bookings = await BookingService.find_all(user_id=user.id)
    if not bookings:
        raise BookingNotFound
    return bookings


@booking_router.post("/create", response_model=BookingResponse)
@cache(expire=30)
async def create_booking(
        room_id: int,
        date_from: date,
        date_to: date,
        user: UserModel = Depends(get_current_user)):
    booking = await BookingService.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked

    adapter = TypeAdapter(BookingSchema)
    booking_dict = adapter.dump_json(booking)
    booking_dict = json.loads(booking_dict.decode("utf-8"))
    send_booking_confirmation.delay(booking_dict, user.email)

    return BookingResponse(message="The room has been successfully booked!")


@booking_router.delete("/delete/{booking_id}", response_model=BookingResponse)
async def delete_booking(booking_id: int, user: UserModel = Depends(get_current_user)):
    booking = await BookingService.delete(id=booking_id, user_id=user.id)
    if not booking:
        raise BookingNotFound
    return BookingResponse(message=f"Booking №{booking.id} of {user.username} was deleted!")
