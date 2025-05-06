import pytest
from httpx import AsyncClient

from config import EMAIL_USER_FOR_TESTS


@pytest.mark.parametrize(
    "username,email,password,status_code",
    [
        ("test", "test@test.ru", "12345678", 200),
        ("test", "test@test.ru", "12345678", 409),
        ("test", "invalid-email", "12345678", 422),
        ("", "", "", 422),
        ("", "test1@test.ru", "12345678", 422),
        ("test", "test@test.ru", "", 422),
    ],
)
@pytest.mark.asyncio
async def test_register_user(username, email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "/v1/auth/register",
        json={"username": username, "email": email, "password": password},
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("test@test.com", "test1", 422),
        ("test@test.com", "test", 200),
        ("", "", 422),
        ("test11231@test.ru", "12345678", 404),
    ],
)
@pytest.mark.asyncio
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/v1/auth/login", json={"email": email, "password": password})
    assert response.status_code == status_code


@pytest.mark.asyncio
async def test_get_me(auth_ac: AsyncClient):
    response = await auth_ac.get("/v1/users/me")
    assert response.json()["email"] == EMAIL_USER_FOR_TESTS


@pytest.mark.asyncio
async def test_logout_user(auth_ac: AsyncClient):
    response = await auth_ac.post("/v1/users/logout")
    assert response.status_code == 200
    assert "booking_access_token" not in auth_ac.cookies
