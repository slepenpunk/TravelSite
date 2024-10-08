import uvicorn
from fastapi import FastAPI
from rooms.router import room_router
from users.router import user_router
from bookings.router import booking_router


app = FastAPI()
app.include_router(room_router)
app.include_router(user_router)
app.include_router(booking_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
