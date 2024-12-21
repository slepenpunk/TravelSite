from fastapi import HTTPException, status

from exceptions.base import BaseHHTPException


class RoomNotFound(BaseHHTPException):
    def __init__(self):
        super().__init__(detail="Room not found!", status_code=status.HTTP_404_NOT_FOUND)


class RoomCannotBeBooked(BaseHHTPException):
    def __init__(self):
        super().__init__(detail="Room already booked!", status_code=status.HTTP_409_CONFLICT)



