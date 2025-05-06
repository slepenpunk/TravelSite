import logging

from fastapi import APIRouter, Depends, Response
from fastapi_cache.decorator import cache

from logger import handle_and_log_errors
from users.auth import auth_user, create_access_token, get_password_hash
from users.dependencies import get_current_user
from users.models import UserModel
from users.schemas import UserAuth, UserIn, UserOut, UserResponse
from users.service import UserService

from .exceptions import *

user_router = APIRouter(prefix="/users", tags=["Users"])
auth_router = APIRouter(prefix="/auth", tags=["Auth"])
logger = logging.getLogger(__name__)


@auth_router.post("/register", response_model=UserResponse)
@handle_and_log_errors(logger=logger)
async def register_user(user: UserIn):
    existing_user = await UserService.find_one_or_none(email=user.email)
    if existing_user:
        raise UserAlreadyExist
    hashed_password = get_password_hash(user.password)
    await UserService.add(
        username=user.username, email=user.email, password=hashed_password
    )
    return UserResponse(message=f"{user.username} successful registered!")


@auth_router.post("/login", response_model=UserResponse)
@handle_and_log_errors(logger=logger)
async def login_user(response: Response, user_data: UserAuth):
    user = await auth_user(user_data.email, user_data.password)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return UserResponse(message=f"{user.id} {user.username} logged in!")


@user_router.post("/logout", response_model=UserResponse)
@handle_and_log_errors(logger=logger)
async def logout_user(response: Response, user: UserModel = Depends(get_current_user)):
    response.delete_cookie("booking_access_token")
    return UserResponse(message=f"{user.id} {user.username} logout.")


@user_router.get("/me", response_model=UserOut)
@cache(expire=30)
@handle_and_log_errors(logger=logger)
async def get_me(user: UserModel = Depends(get_current_user)):
    return user
