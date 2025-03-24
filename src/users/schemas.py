from pydantic import BaseModel, EmailStr, ConfigDict, Field, ValidationError


class UserSchema(BaseModel):
    username: str = Field(min_length=2, max_length=32)
    email: EmailStr

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True
    )


class UserIn(UserSchema):
    try:
        password: str = Field(min_length=8, max_length=32)
    except ValueError as e:
        raise ValidationError(str(e))


class UserAuth(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    message: str

