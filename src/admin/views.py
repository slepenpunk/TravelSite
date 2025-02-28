from email_validator import validate_email, EmailNotValidError

from sqladmin import ModelView

from bookings.models import BookingModel
from hotels.models import HotelModel
from rooms.models import RoomModel
from users.auth import get_password_hash
from users.exceptions import IncorrectEmailFormat
from users.models import UserModel
from users.router import register_user
from users.schemas import UserSchema, UserIn
from users.service import UserService


def is_valid_email(email):
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False


class UserAdmin(ModelView, model=UserModel):
    name = "User"
    name_plural = "Users"
    column_list = [UserModel.id, UserModel.email]
    column_details_exclude_list = [UserModel.password]
    can_delete = True

    async def on_model_change(self, data, model, is_created, request):
        data["password"] = get_password_hash(data["password"])


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
