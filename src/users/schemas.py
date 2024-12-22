from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    username: str
    email: EmailStr

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class UserIn(UserSchema):
    password: str


class UserAuth(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    message: str

