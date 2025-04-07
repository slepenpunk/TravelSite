from fastapi import status

from exceptions.base import BaseHHTPException


class BookingNotFound(BaseHHTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND,
                         detail="Booking not found!")


class InvalidBookingDate(BaseHHTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_409_CONFLICT,
                         detail="Invalid date!")


class BookingAlreadyBooked(BaseHHTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_409_CONFLICT,
                         detail="Booking already booked!")
