from sqladmin import ModelView

from bookings.models import BookingModel
from hotels.models import HotelModel
from rooms.models import RoomModel
from users.models import UserModel


class UserAdmin(ModelView, model=UserModel):
    name = "User"
    name_plural = "Users"
    column_list = [UserModel.id, UserModel.email]
    column_details_exclude_list = [UserModel.password]
    can_delete = False


class BookingAdmin(ModelView, model=BookingModel):
    name = "Booking"
    name_plural = "Bookings"
    column_list = [i.name for i in BookingModel.__table__.c] + [BookingModel.user]


class RoomAdmin(ModelView, model=RoomModel):
    name = "Room"
    name_plural = "Rooms"
    column_list = [i.name for i in RoomModel.__table__.c]


class HotelAdmin(ModelView, model=HotelModel):
    name = "Hotel"
    name_plural = "Hotels"
    column_list = [i.name for i in HotelModel.__table__.c]

