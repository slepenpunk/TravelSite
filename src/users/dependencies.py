import datetime

from fastapi import Depends, Request
from jose import JWTError, jwt

from config import SECRET_KEY
from users.service import UserService

from .exceptions import *


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenNotFound
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, SECRET_KEY)
    except JWTError:
        raise IncorrectTokenFormat
    expire: str = payload.get("exp")
    if not expire or int(expire) < datetime.datetime.now(datetime.UTC).timestamp():
        raise TokenExpired
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsAbsent
    user = await UserService.find_by_id(int(user_id))
    if not user:
        raise UserIsAbsent
    return user
