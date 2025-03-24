from bookings.service import BookingService
from exceptions.base import BaseHHTPException

import pytest
from datetime import datetime, timezone


@pytest.mark.asyncio
@pytest.mark.parametrize("user_id, room_id, date_from, date_to, expected_result", [
    # Позитивный сценарий: бронируем свободный номер
    (1, 2, "2030-03-21", "2030-03-22", True),

    # Негативные сценарии:
    # Попытка забронировать уже занятый room_id=1 на пересекающиеся даты
    (3, 1, "2025-03-26", "2025-03-28", False),

    # Попытка забронировать уже занятый room_id=3 на пересекающиеся даты
    (3, 3, "2025-04-05", "2025-04-07", False),

    # Попытка забронировать room_id=3 до начала существующей брони, но с пересечением
    (3, 3, "2025-03-30", "2025-04-03", False),

    # Неверный user_id
    (999, 1, "2025-05-01", "2025-05-22", False),

    # Неверный room_id
    (1, 999, "2025-05-01", "2025-05-22", False),

    # Неверные даты
    (1, 2, "2025-03-10", "2025-03-05", False),

    # Один день бронирования
    (1, 2, "2025-03-01", "2025-03-01", False),
])
async def test_add_and_get_booking(user_id, room_id, date_from, date_to, expected_result):
    try:
        date_from = datetime.strptime(date_from, "%Y-%m-%d").date()
        date_to = datetime.strptime(date_to, "%Y-%m-%d").date()
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
