import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_versioning import VersionedFastAPI
from redis import asyncio as aioredis
from sqladmin import Admin

from admin.auth import authentication_backend
from admin.views import BookingAdmin, HotelAdmin, RoomAdmin, UserAdmin
from bookings.router import booking_router
from config import REDIS_URL
from database import engine
from hotels.router import hotel_router
from images.router import image_router
from logger import base_logger
from pages.router import page_router
from rooms.router import room_router
from users.router import auth_router, user_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(REDIS_URL)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield


base_app = FastAPI(lifespan=lifespan)

base_app.include_router(room_router)
base_app.include_router(user_router)
base_app.include_router(auth_router)
base_app.include_router(booking_router)
base_app.include_router(hotel_router)
base_app.include_router(page_router)
base_app.include_router(image_router)

app = VersionedFastAPI(
    app=base_app, version_format="{major}", prefix_format="/v{major}", lifespan=lifespan
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    base_logger.info(
        "Request execution time:", extra={"process_time": round(process_time, 4)}
    )
    return response


@app.middleware("http")
async def log_middleware(request: Request, call_next):
    response = await call_next(request)
    base_logger.info(
        f"Direct to: {request.url}", extra={"status_code": response.status_code}
    )
    return response


admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(BookingAdmin)
admin.add_view(RoomAdmin)
admin.add_view(HotelAdmin)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
