import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("username,email,password,status_code", [
    ("test", "test@test.ru", "12345678", 200),
    ("test", "test@test.ru", "12345678", 409),
    ("test", "invalid-email", "12345678", 422),
    ("", "", "", 422),
    ("", "test1@test.ru", "12345678", 422),
    ("test", "no@password.ru", "", 422),
])
@pytest.mark.asyncio
async def test_register_user(username, email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "username": username,
        "email": email,
        "password": password
    })
    print(ac)
    assert response.status_code == status_code


@pytest.mark.parametrize("email,password,status_code", [
    ("test@test.com", "test1", 422),
    ("test@test.com", "test", 200),
    ("", "", 422),
])
@pytest.mark.asyncio
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/login", json={
        "email": email,
        "password": password
    })
    assert response.status_code == status_code
