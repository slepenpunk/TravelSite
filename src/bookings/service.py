from datetime import date

from sqlalchemy import select, and_, or_, insert

from bookings.exceptions import InvalidBookingDate
from bookings.models import BookingModel
from database import async_session_maker
from rooms.exceptions import RoomNotFound
from rooms.models import RoomModel

from services.base import BaseService


class BookingService(BaseService):
    model = BookingModel

    @classmethod
    async def check_available_booking(cls, room_id, date_from, date_to):
        if date_from > date_to:
            raise InvalidBookingDate
        async with async_session_maker() as session:
            get_booking = select(BookingModel).where(
                and_(
                    BookingModel.room_id == room_id,
                    or_(
                        and_(
                            BookingModel.date_from >= date_from,
                            BookingModel.date_from <= date_to
                        ),
                        and_(
                            BookingModel.date_from <= date_from,
                            BookingModel.date_to > date_from
                        )
                    )
                )
            )
        get_booking = await session.execute(get_booking)

        if get_booking.scalars().first():
            return None
        return True

    @classmethod
    async def add(cls, user_id: int, room_id: int, date_from: date, date_to: date):
        from rooms.service import RoomService

        get_room = await RoomService.find_one_or_none(id=room_id)
        if get_room is None or get_room.hotel_id is None:
            raise RoomNotFound

        is_available = await cls.check_available_booking(room_id=room_id,
                                                         date_from=date_from,
                                                         date_to=date_to)

        if is_available is True:
            async with async_session_maker() as session:
                get_price = select(RoomModel.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_booking = insert(BookingModel).values(
                    user_id=user_id,
                    room_id=room_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price
                ).returning(BookingModel)
                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking
