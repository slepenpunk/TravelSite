from datetime import date

from sqlalchemy import select, and_, or_, insert

from bookings.models import BookingModel
from database import async_session_maker
from rooms.exceptions import RoomIsNotFound
from rooms.models import RoomModel
from services.base import BaseService


class BookingService(BaseService):
    model = BookingModel

    @classmethod
    async def add(cls,
                  user_id: int,
                  room_id: int,
                  date_from: date,
                  date_to: date):
        async with async_session_maker() as session:
            room_check = select(RoomModel).where(RoomModel.id == room_id)
            room_exists = await session.execute(room_check)
            room_exists = room_exists.scalar()

            if room_exists is None or room_exists.hotel_id is None:
                raise RoomIsNotFound

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

            if get_booking.first():
                return None

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
            return new_booking.scalar()
