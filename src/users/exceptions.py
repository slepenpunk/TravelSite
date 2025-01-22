from exceptions.base import BaseHHTPException
from fastapi import status


class UserAlreadyExist(BaseHHTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail="User already exist!")


class UserAlreadyLogged(BaseHHTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail="User already logged!")


class UserNotFound(BaseHHTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found!")


class IncorrectPassword(BaseHHTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password!")


class TokenExpired(BaseHHTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token time is expire!")


class TokenNotFound(BaseHHTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found!")


class IncorrectTokenFormat(BaseHHTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect token format!")


class UserIsAbsent(BaseHHTPException):
    def __init__(self, detail=None):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class AccessDenied(BaseHHTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied!")
