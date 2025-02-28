import asyncio
import datetime
import json

import pytest
from sqlalchemy import insert

from database import Base, async_session_maker, engine
from config import MODE
from bookings.models import BookingModel
from main import app
from rooms.models import RoomModel
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


# @pytest.fixture(scope="session")
# def event_loop(request):
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(base_url="http://test", transport=ASGITransport(app=app)) as ac:
        yield ac


@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session
