from fastapi import status

from exceptions.base import BaseHHTPException


class UserAlreadyExist(BaseHHTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT, detail="User already exist!"
        )


class UserAlreadyLogged(BaseHHTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT, detail="User already logged!"
        )


class UserNotFound(BaseHHTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found!"
        )


class IncorrectPassword(BaseHHTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Incorrect password!",
        )


class TokenExpired(BaseHHTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token time is expire!"
        )


class TokenNotFound(BaseHHTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found!"
        )


class IncorrectTokenFormat(BaseHHTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect token format!"
        )


class UserIsAbsent(BaseHHTPException):
    def __init__(self, detail=None):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class AccessDenied(BaseHHTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied!")


class IncorrectEmailFormat(BaseHHTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Incorrect e-mail format!",
        )


class IncorrectUsernameFormat(BaseHHTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Username length must be between 2 and 32 characters!",
        )


class IncorrectPasswordFormat(BaseHHTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password length must be between 8 and 32 characters!",
        )
