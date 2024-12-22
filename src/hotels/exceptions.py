from exceptions.base import BaseHHTPException


class HotelNotFound(BaseHHTPException):
    def __init__(self, detail: str = "Hotel not found!"):
        super().__init__(status_code=404, detail=detail)


class CityNotFound(BaseHHTPException):
    def __init__(self, detail: str = "City not found!"):
        super().__init__(detail=detail, status_code=404)
