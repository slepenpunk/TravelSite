from fastapi import HTTPException, status

BookingNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Booking not found!"
)