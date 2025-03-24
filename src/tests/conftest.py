import datetime
import json

import pytest
from fakeredis import aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.backends.redis import RedisBackend
from sqlalchemy import insert

from database import Base, async_session_maker, engine
from config import MODE
from bookings.models import BookingModel
from main import app
from rooms.models import RoomModel
from users.auth import get_password_hash
from users.models import UserModel
from hotels.models import HotelModel
from httpx import AsyncClient, ASGITransport


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    hotels = open_mock_json("hotels")
    rooms = open_mock_json("rooms")
    users = open_mock_json("users")
    bookings = open_mock_json("bookings")

    for user in users:
        user["password"] = get_password_hash(user["password"])

    for booking in bookings:
        booking["date_from"] = datetime.datetime.strptime(booking["date_from"], "%Y-%m-%d")
        booking["date_to"] = datetime.datetime.strptime(booking["date_to"], "%Y-%m-%d")

    async with async_session_maker() as session:
        add_hotels = insert(HotelModel).values(hotels)
        add_rooms = insert(RoomModel).values(rooms)
        add_users = insert(UserModel).values(users)
        add_bookings = insert(BookingModel).values(bookings)

        await session.execute(add_hotels)
        await session.execute(add_rooms)
        await session.execute(add_users)
        await session.execute(add_bookings)

        await session.commit()


@pytest.fixture(scope="session", autouse=True)
async def init_cache():
    redis = aioredis.FakeRedis()
    FastAPICache.init(RedisBackend(redis), prefix="cache")


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(base_url="http://test", transport=ASGITransport(app=app)) as ac:
        yield ac


@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session
