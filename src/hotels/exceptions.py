from exceptions.base import BaseHHTPException


class HotelNotFound(BaseHHTPException):
    def __init__(self, detail: str = "Hotel not found!"):
        super().__init__(status_code=404, detail=detail)


class LocationNotFound(BaseHHTPException):
    def __init__(self, detail: str = "Location not found!"):
        super().__init__(detail=detail, status_code=404)
