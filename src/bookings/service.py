import logging
from datetime import date, datetime, timezone
from typing import Optional

from sqlalchemy import and_, insert, or_, select, update

from bookings.exceptions import InvalidBookingDate
from bookings.models import BookingModel
from database import async_session_maker
from rooms.exceptions import RoomCannotBeBooked, RoomNotFound
from rooms.models import RoomModel
from services.base import BaseService
from users.exceptions import UserNotFound
from users.service import UserService


class BookingService(BaseService):
    model = BookingModel

    @classmethod
    async def check_available_booking(
            cls,
            room_id: int,
            date_from: date,
            date_to: date,
            exclude_booking_id: int = None,
    ) -> bool:

        from rooms.service import RoomService

        existing_room = await RoomService.find_one_or_none(id=room_id)
        if not existing_room:
            raise RoomNotFound

        utc_now = datetime.now(timezone.utc).date()
        if date_from >= date_to or date_from < utc_now:
            raise InvalidBookingDate

        async with async_session_maker() as session:
            conditions = [
                BookingModel.room_id == room_id,
                or_(
                    and_(
                        BookingModel.date_from >= date_from,
                        BookingModel.date_from <= date_to,
                    ),
                    and_(
                        BookingModel.date_from <= date_from,
                        BookingModel.date_to > date_from,
                    ),
                ),
            ]

            if exclude_booking_id:
                conditions.append(BookingModel.id != exclude_booking_id)

            get_booking = select(BookingModel).where(and_(*conditions))
            get_booking = await session.execute(get_booking)

        if get_booking.scalars().first():
            return False
        return True

    @classmethod
    async def add(
            cls,
            user_id: int,
            room_id: int,
            date_from: date,
            date_to: date
    ) -> Optional[BookingModel]:

        from rooms.service import RoomService

        get_room = await RoomService.find_one_or_none(id=room_id)
        if get_room is None or get_room.hotel_id is None:
            raise RoomNotFound
        is_available = await cls.check_available_booking(
            room_id=room_id, date_from=date_from, date_to=date_to
        )

        get_user = await UserService.find_by_id(user_id)
        if not get_user:
            raise UserNotFound

        if is_available is True:
            async with async_session_maker() as session:
                get_price = select(RoomModel.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_booking = (
                    insert(cls.model)
                    .values(
                        user_id=user_id,
                        room_id=room_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=price,
                    )
                    .returning(cls.model)
                )
                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()

    @classmethod
    async def update(cls, item_id: int, **data) -> Optional[BookingModel]:

        async with async_session_maker() as session:
            user_id = data["user_id"]
            room_id = data["room_id"]
            date_from = data["date_from"]
            date_to = data["date_to"]
            exists_booking = await cls.find_one_or_none(id=item_id, user_id=user_id)

            if exists_booking is None:
                return None

            is_available = await cls.check_available_booking(
                room_id=room_id,
                date_from=date_from,
                date_to=date_to,
                exclude_booking_id=item_id,
            )
            if is_available is False:
                raise RoomCannotBeBooked
            stmt = (
                update(cls.model)
                .where(cls.model.id == item_id)
                .values(room_id=room_id, date_from=date_from, date_to=date_to)
                .returning(cls.model)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one_or_none()
