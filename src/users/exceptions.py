from fastapi import HTTPException, status

UserAlreadyExist = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User already exist!"
)

UserNotFound = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User not found!"
)

IncorrectPassword = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect password!"
)

TokenExpired = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token time is expire!"
)

TokenNotFound = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token not found!"
)

IncorrectTokenFormat = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect token format!"
)

UserIsAbsent = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED
)
