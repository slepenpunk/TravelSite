from typing import Any

from email_validator import EmailNotValidError, validate_email
from pydantic import ValidationError
from sqladmin import ModelView
from starlette.requests import Request

from bookings.exceptions import BookingAlreadyBooked
from bookings.models import BookingModel
from bookings.service import BookingService
from hotels.models import HotelModel
from rooms.models import RoomModel
from rooms.service import RoomService
from users.auth import get_password_hash
from users.exceptions import UserAlreadyExist
from users.models import UserModel
from users.schemas import UserIn
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
    form_columns = ["username", "email", "password"]

    can_delete = True

    async def on_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        try:
            new_email = data.get("email")
            new_username = data.get("username")
            new_password = data.get("password")

            user_schema = UserIn(
                email=new_email, username=new_username, password=new_password
            )

            if user_schema.email:
                existing_user = await UserService.find_one_or_none(
                    email=user_schema.email
                )
                if existing_user and (is_created or existing_user.id != model.id):
                    raise UserAlreadyExist

            if new_password:
                data["password"] = get_password_hash(user_schema.password)
        except ValidationError as e:
            errors = e.errors()
            error_messages = []

            for error in errors:
                field = error["loc"][0]
                msg = error["msg"]
                error_messages.append(f"{field}: {msg}")

            formatted_errors = "; ".join(error_messages)
            raise ValueError(formatted_errors)


class BookingAdmin(ModelView, model=BookingModel):
    name = "Booking"
    name_plural = "Bookings"
    column_list = [i.name for i in BookingModel.__table__.c] + [BookingModel.user]
    form_columns = ["user", "room", "date_from", "date_to"]

    async def on_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:

        room_id = data.get("room")
        date_from = data.get("date_from")
        date_to = data.get("date_to")
        is_available = await BookingService.check_available_booking(
            room_id=int(room_id), date_from=date_from, date_to=date_to
        )
        if is_available:
            get_room = await RoomService.find_by_id(int(room_id))
            data["price"] = get_room.price
        else:
            raise BookingAlreadyBooked


class RoomAdmin(ModelView, model=RoomModel):
    name = "Room"
    name_plural = "Rooms"
    column_list = [i.name for i in RoomModel.__table__.c]
    form_columns = ["hotel", "name", "price"]


class HotelAdmin(ModelView, model=HotelModel):
    name = "Hotel"
    name_plural = "Hotels"
    column_list = [i.name for i in HotelModel.__table__.c]
