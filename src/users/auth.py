import datetime

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from config import SECRET_KEY
from users.service import UserService

from .exceptions import *

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hash_password):
    return pwd_context.verify(plain_password, hash_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY)
    return encoded_jwt


async def auth_user(email: EmailStr, password: str):
    user = await UserService.find_one_or_none(email=email)
    if not user:
        raise UserNotFound
    if user and verify_password(password, user.password) is False:
        raise IncorrectPassword
    return user
