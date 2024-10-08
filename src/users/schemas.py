from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    username: str | None = "123"
    email: EmailStr
    password: str

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class UserAuth(BaseModel):
    email: EmailStr
    password: str
