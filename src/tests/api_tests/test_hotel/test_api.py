import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "city, expected_status ", [("несуществующий город", 404), ("Сочи", 200)]
)
async def test_get_hotels_by_city(city: str, expected_status: int, ac: AsyncClient):
    response = await ac.get(f"/v1/hotels/{city}")
    assert response.status_code == expected_status


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "hotel, expected_status ",
    [
        ("Seaside Resort", 200),
        ("No exists", 404),
    ],
)
async def test_get_rooms_of_hotel(hotel: int, expected_status: int, ac: AsyncClient):
    response = await ac.get(f"/v1/hotels/{hotel}/rooms")
    assert response.status_code == expected_status
