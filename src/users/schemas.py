from pydantic import BaseModel, EmailStr, ConfigDict


class UserSchema(BaseModel):
    username: str
    email: EmailStr

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True
    )


class UserIn(UserSchema):
    password: str


class UserAuth(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    message: str

