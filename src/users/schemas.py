import datetime

from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    id: int | None = None
    username: str | None = "123"
    email: EmailStr
    password: str

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class UserRegisterSchema(BaseModel):
    email: EmailStr
