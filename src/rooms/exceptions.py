from fastapi import HTTPException, status

RoomCannotBeBooked = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Room already booked!"
)

RoomIsNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Room not found!"
)

