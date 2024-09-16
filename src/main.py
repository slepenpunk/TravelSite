import uvicorn
from fastapi import FastAPI
from rooms.routers import room_router
from users.routers import user_router

app = FastAPI()
app.include_router(room_router)
app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
