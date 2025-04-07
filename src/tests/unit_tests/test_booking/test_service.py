from fastapi import Depends

from bookings.schemas import BookingSchema, BookingIn
from bookings.service import BookingService
from exceptions.base import BaseHHTPException

import pytest
from datetime import datetime


@pytest.mark.asyncio
@pytest.mark.parametrize("user_id, room_id, date_from, date_to, expected_result", [
    (1, 1, "2026-01-01", "2026-01-21", True),
    (1, 1, "2027-01-21", "2027-02-01", True),
    (1, 1, "2026-01-01", "2026-01-21", False),
    (1, 1, "2000-01-01", "2000-01-21", False),
    (1, 100, "2028-01-01", "2028-01-21", False),
    (1, 1, "", "2031-01-01", False),
    (1, 3, "2025-05-02", "2025-05-04", False)
])
async def test_add_and_get_booking(user_id, room_id, date_from, date_to, expected_result):
    try:
        if date_from and date_to:
            date_from = datetime.strptime(date_from, "%Y-%m-%d").date()
            date_to = datetime.strptime(date_to, "%Y-%m-%d").date()
        else:
            date_from, date_to = "", ""

        new_booking = await BookingService.add(user_id, room_id, date_from, date_to)
        if expected_result:
            assert new_booking is not None
            assert new_booking.user_id == user_id
            assert new_booking.room_id == room_id

            found_booking = await BookingService.find_by_id(new_booking.id)
            assert found_booking is not None
        else:
            assert new_booking is None
    except BaseHHTPException:
        assert not expected_result


@pytest.mark.asyncio
@pytest.mark.parametrize("booking_id, user_id, room_id, date_from, date_to, expected_result", [
    (1, 1, 1, "2025-05-25", "2025-05-27", True),
    (3, 1, 1, "2026-02-01", "2026-02-10", True),
    (1, 1, 1, "2025-05-20", "2025-05-30", True),
    (1, 1, 2, "2025-05-25", "2025-05-27", True),
    (1, 1, 3, "2025-05-01", "2025-05-05", False),
    (2, 1, 3, "2025-05-03", "2025-05-07", False),
    (1, 1, 1, "2025-05-30", "2025-05-25", False),
    (1, 1, 1, "2020-01-01", "2020-01-10", False),
    (1, 1, 999, "2025-05-25", "2025-05-27", False)
])
async def test_update_booking(booking_id, user_id, room_id, date_from, date_to, expected_result):
    try:
        if date_from and date_to:
            date_from = datetime.strptime(date_from, "%Y-%m-%d").date()
            date_to = datetime.strptime(date_to, "%Y-%m-%d").date()
        else:
            date_from, date_to = "", ""

        updating_booking = await BookingService.update(item_id=booking_id,
                                                       room_id=room_id,
                                                       user_id=user_id,
                                                       date_from=date_from,
                                                       date_to=date_to)
        if expected_result:
            assert updating_booking is not None
            check_updated_booking = await BookingService.find_by_id(booking_id)
            assert check_updated_booking
            assert check_updated_booking.room_id == updating_booking.room_id
            assert check_updated_booking.date_from == updating_booking.date_from
            assert check_updated_booking.date_to == updating_booking.date_to
        else:
            assert updating_booking is None

    except BaseHHTPException:
        assert not expected_result
