import pytest
from httpx import AsyncClient
from urllib.parse import quote


@pytest.mark.asyncio
async def test_get_hotels(ac: AsyncClient):
    response = await ac.get("/hotels")
    assert response.status_code == 200
    assert response.json()


@pytest.mark.asyncio
@pytest.mark.parametrize("city, expected_status ", [
    ("несуществующий город", 404),
    ("Сочи", 200)
])
async def test_get_hotels_by_city(city: str, expected_status: int, ac: AsyncClient):
    response = await ac.get(f"/hotels/{city}")
    assert response.status_code == expected_status

