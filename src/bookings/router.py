from datetime import date

from fastapi import APIRouter, Depends

from bookings.exceptions import BookingNotFound
from bookings.schemas import BookingSchema, BookingResponse
from bookings.service import BookingService
from rooms.exceptions import RoomCannotBeBooked
from users.dependencies import get_current_user
from users.models import UserModel

booking_router = APIRouter(prefix="/bookings", tags=["Bookings"])


@booking_router.get("", response_model=list[BookingSchema])
async def get_bookings(user: UserModel = Depends(get_current_user)):
    bookings = await BookingService.find_all(user_id=user.id)
    if not bookings:
        raise BookingNotFound
    return bookings


@booking_router.post("/create", response_model=BookingResponse)
async def create_booking(
        room_id: int,
        date_from: date,
        date_to: date,
        user: UserModel = Depends(get_current_user)):
    booking = await BookingService.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked
    return BookingResponse(message="OK")


@booking_router.delete("/delete/{booking_id}", response_model=BookingResponse)
async def delete_booking(booking_id: int, user: UserModel = Depends(get_current_user)):
    booking = await BookingService.delete(id=booking_id, user_id=user.id)
    if not booking:
        raise BookingNotFound
    return BookingResponse(message=f"Booking №{booking.id} of {user.username} was deleted!")
