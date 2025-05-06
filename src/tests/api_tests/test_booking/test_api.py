import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_bookings(auth_ac: AsyncClient):
    response = await auth_ac.get("/v1/bookings")
    assert response.status_code == 200
    assert response.json()[0]["user_id"] == 1


@pytest.mark.parametrize(
    "room_id,date_from,date_to,status_code",
    [
        (1, "2026-01-01", "2026-01-21", 200),
        (1, "2027-01-01", "2027-01-21", 200),
        (1, "2026-01-01", "2026-01-21", 409),
        (1, "2000-01-01", "2000-01-21", 409),
        (100, "2028-01-01", "2028-01-21", 404),
        (1, "", "2031-01-01", 409),
        (3, "2025-05-02", "2025-05-04", 409),
    ],
)
@pytest.mark.asyncio
async def test_create_booking(room_id, date_from, date_to, status_code, auth_ac: AsyncClient):
    get_me = await auth_ac.get("/v1/users/me")
    user_id = get_me.json()["id"]
    response = await auth_ac.post(
        "/v1/bookings/create",
        json={
            "user_id": user_id,
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert response.status_code == status_code
    if response.status_code == 200:
        bookings = await auth_ac.get("/v1/bookings")
        bookings_json = bookings.json()
        for booking in bookings_json:
            if (
                    booking["user_id"] == user_id
                    and booking["room_id"] == room_id
                    and booking["date_from"] == date_from
                    and booking["date_to"] == date_to
            ):
                assert booking["user_id"] == user_id
                assert booking["room_id"] == room_id
                assert booking["date_from"] == date_from
                assert booking["date_to"] == date_to


@pytest.mark.parametrize(
    "booking_id,room_id,date_from,date_to,status_code",
    [
        # 1. Уменьшение периода бронирования
        (1, 1, "2025-05-25", "2025-05-27", 200),
        # 2. Расширение периода без конфликтов
        (1, 1, "2025-05-20", "2025-05-30", 200),
        # 3. Конфликт с чужим бронированием
        (1, 3, "2025-05-01", "2025-05-05", 409),
        # 4. Попытка изменить бронирование другого пользователя
        (2, 3, "2025-05-03", "2025-05-07", 404),
        # 5. Некорректные даты (дата окончания раньше даты начала)
        (1, 1, "2025-05-30", "2025-05-25", 409),
        (1, 1, "", "2025-05-27", 409),
        # 6. Бронирование в прошлом
        (1, 1, "2020-01-01", "2020-01-10", 409),
        # 7. Перенос бронирования на свободные даты
        (3, 1, "2026-02-01", "2026-02-10", 200),
        # 8. Конфликт при переносе на занятые даты
        (4, 1, "2025-05-25", "2025-05-27", 409),
        # 9. Изменение комнаты на доступную
        (1, 2, "2025-05-25", "2025-05-27", 200),
        # 10. Несуществующая комната
        (1, 999, "2025-05-25", "2025-05-27", 404),
    ],
)
@pytest.mark.asyncio
async def test_update_booking(
        booking_id, room_id, date_from, date_to, status_code, auth_ac: AsyncClient
):
    get_me = await auth_ac.get("/v1/users/me")
    user_id = get_me.json()["id"]
    updating_booking = {
        "booking_id": booking_id,
        "user_id": user_id,
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to,
    }

    response = await auth_ac.patch(f"/v1/bookings/update/{booking_id}", json=updating_booking)
    assert response.status_code == status_code
    if response.status_code == 200:
        get_bookings = await auth_ac.get("/v1/bookings")
        for booking in get_bookings.json():
            if booking["id"] == booking_id:
                assert booking["room_id"] == room_id
                assert booking["date_from"] == date_from
                assert booking["date_to"] == date_to
