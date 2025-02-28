import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "username": "test",
        "email": "test1@test.com",
        "password": "test"
    })
    assert response.status_code == 200
