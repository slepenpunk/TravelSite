from bookings.models import BookingModel
from services.base import BaseService


class BookingService(BaseService):
    model = BookingModel
