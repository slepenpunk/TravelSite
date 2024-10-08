import datetime

from fastapi import Request, Depends
from jose import jwt, JWTError
from config import SECRET_KEY
from exceptions import Exceptions
from users.service import UserService


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise Exceptions.TokenNotFound
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, SECRET_KEY)
    except JWTError:
        raise Exceptions.IncorrectTokenFormat
    expire: str = payload.get("exp")
    if not expire or int(expire) < datetime.datetime.now(datetime.UTC).timestamp():
        raise Exceptions.TokenExpired
    user_id: str = payload.get("sub")
    if not user_id:
        raise Exceptions.UserIsAbsent
    user = await UserService.find_by_id(int(user_id))
    if not user:
        raise Exceptions.UserIsAbsent
    return user
