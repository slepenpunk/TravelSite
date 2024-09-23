from fastapi import APIRouter, HTTPException

from users.auth import get_password_hash
from users.service import UserService
from users.schemas import UserSchema, UserRegisterSchema

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.get("/get-users")
async def get_all_users() -> list[UserSchema]:
    query = await UserService.find_all()
    return query


@user_router.get("/{user_id}")
async def get_user_by_id(user_id: int):
    query = await UserService.find_by_id(user_id)
    return query


@user_router.post("/register")
async def register_user(user: UserSchema):
    existing_user = await UserService.find_one_or_none(email=user.email)
    if existing_user:
        raise HTTPException(status_code=400)
    hashed_password = get_password_hash(user.email)
    await UserService.add(username=user.username,
                          email=user.email,
                          password=hashed_password)
    return {"message": "OK"}
