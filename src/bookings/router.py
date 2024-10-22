from datetime import date

from fastapi import APIRouter, Depends

from bookings.exceptions import BookingNotFound
from bookings.schemas import BookingSchema
from bookings.service import BookingService
from rooms.exceptions import RoomCannotBeBooked
from users.dependencies import get_current_user
from users.models import UserModel

booking_router = APIRouter(prefix="/bookings", tags=["Bookings"])


@booking_router.get("/get")
async def get_bookings(user: UserModel = Depends(get_current_user)) -> list[BookingSchema]:
    return await BookingService.find_all(user_id=user.id)


@booking_router.post("/create")
async def create_booking(
        room_id: int, date_from: date, date_to: date,
        user: UserModel = Depends(get_current_user)):
    booking = await BookingService.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked


@booking_router.delete("/delete")
async def delete(booking_id: int):
    get_booking = await BookingService.delete_by_id(booking_id)
    if not get_booking:
        raise BookingNotFound
    return {"message": f"{get_booking.id} was deleted!"}
