from fastapi import APIRouter, Depends

from bookings.schemas import BookingSchema
from bookings.service import BookingService
from users.dependencies import get_current_user
from users.models import UserModel

booking_router = APIRouter(prefix="/bookings", tags=["Bookings"])


@booking_router.get("/get-bookings")
async def get_bookings(user: UserModel = Depends(get_current_user)) -> list[BookingSchema]:
    return await BookingService.find_all(user_id=user.id)