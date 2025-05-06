import re

from pydantic import BaseModel, ConfigDict, Field, field_validator

from users.exceptions import *


class UserSchema(BaseModel):
    username: str = Field(min_length=2, max_length=32)
    email: str

    @field_validator("username", mode="before")
    @classmethod
    def validate_username(cls, value):
        if not (2 <= len(value) <= 32):
            raise IncorrectUsernameFormat
        return value

    @field_validator("email", mode="before")
    @classmethod
    def validate_email(cls, value):
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_regex, value):
            raise IncorrectEmailFormat
        return value

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class UserIn(UserSchema):
    password: str = Field(min_length=8, max_length=32)

    @field_validator("password", mode="before")
    @classmethod
    def validate_password(cls, value):
        if not (8 <= len(value) <= 32):
            raise IncorrectPasswordFormat
        return value


class UserOut(UserSchema):
    id: int


class UserAuth(BaseModel):
    email: str
    password: str

    @field_validator("email", mode="before")
    @classmethod
    def validate_email(cls, value):
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_regex, value):
            raise IncorrectEmailFormat()
        return value


class UserResponse(BaseModel):
    message: str
