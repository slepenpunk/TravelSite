from fastapi import HTTPException, status

HotelNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Hotel not found!"
)
