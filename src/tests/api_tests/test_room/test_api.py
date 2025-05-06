import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "max_price,min_price,expected_status",
    [
        (5000, 0, 200),
        (0, 0, 404),
    ],
)
async def test_get_rooms_by_price(max_price, min_price, expected_status, ac: AsyncClient):
    response = await ac.get(
        "/v1/rooms/price", params={"max_price": max_price, "min_price": min_price}
    )
    assert response.status_code == expected_status
