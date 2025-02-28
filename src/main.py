import subprocess
import os

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from admin.auth import authentication_backend
from admin.views import UserAdmin, BookingAdmin, RoomAdmin, HotelAdmin
from database import engine
from redis import asyncio as aioredis
from sqladmin import Admin

from images.router import image_router
from rooms.router import room_router
from users.router import user_router, auth_router
from bookings.router import booking_router
from hotels.router import hotel_router
from pages.router import page_router

from config import REDIS_URL


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(f"{REDIS_URL}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(room_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(booking_router)
app.include_router(hotel_router)
app.include_router(page_router)
app.include_router(image_router)


admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(BookingAdmin)
admin.add_view(RoomAdmin)
admin.add_view(HotelAdmin)

redis_path = r"D:\Redis\redis-server.exe"  # Укажите правильный путь к redis-server
if not os.path.exists(redis_path):
    print(f"Redis не найден по пути: {redis_path}")
    exit(1)

try:
    redis_process = subprocess.Popen([redis_path])
    print(f"Redis запущен.")
except Exception as e:
    print(f"Ошибка при запуске Redis: {e}")
    exit(1)

if __name__ == "__main__":
    try:
        uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    finally:
        redis_process.terminate()
        print("Redis завершен.")
