from fastapi import APIRouter, Response, Depends
from starlette.responses import JSONResponse

from .exceptions import *
from users.auth import get_password_hash, auth_user, create_access_token
from users.dependencies import get_current_user
from users.models import UserModel
from users.service import UserService
from users.schemas import UserSchema, UserAuth, UserIn, LoginResponse, RegisterResponse

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.get("/get-users", response_model=list[UserSchema])
async def get_all_users():
    query = await UserService.find_all()
    if not query:
        raise UserNotFound
    return query


@user_router.post("/register", response_model=RegisterResponse)
async def register_user(user: UserIn):
    existing_user = await UserService.find_one_or_none(email=user.email)
    print(existing_user)
    if existing_user:
        raise UserAlreadyExist
    hashed_password = get_password_hash(user.password)
    await UserService.add(username=user.username,
                          email=user.email,
                          password=hashed_password)
    return RegisterResponse(message=f"{user.username} successful registered!")


@user_router.post("/login", response_model=LoginResponse)
async def login_user(response: Response, user_data: UserAuth):
    user = await auth_user(user_data.email, user_data.password)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return LoginResponse(message=f'{user.id} {user.username} logged in!')


@user_router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")


@user_router.get("/me", response_model=UserSchema)
async def get_me(user: UserModel = Depends(get_current_user)):
    return user
