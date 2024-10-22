from fastapi import APIRouter, Response, Depends

from .exceptions import *
from users.auth import get_password_hash, auth_user, create_access_token
from users.dependencies import get_current_user
from users.models import UserModel
from users.service import UserService
from users.schemas import UserSchema, UserAuth

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.get("/get-users")
async def get_all_users():
    query = await UserService.find_all()
    return query


@user_router.post("/register")
async def register_user(user: UserSchema):
    existing_user = await UserService.find_one_or_none(email=user.email)
    if existing_user:
        raise UserAlreadyExist
    hashed_password = get_password_hash(user.password)
    await UserService.add(username=user.username,
                          email=user.email,
                          password=hashed_password)
    return {"message": "OK"}


@user_router.post("/login")
async def login_user(response: Response, user_data: UserAuth):
    user = await auth_user(user_data.email, user_data.password)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return f'{user.id} {user.username} logged in!'


@user_router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")


@user_router.get("/me")
async def get_user(user: UserModel = Depends(get_current_user)):
    return user



