from database import async_session_maker
from users.models import UserModel
from services.base import BaseService
from users.schemas import UserSchema


class UserService(BaseService):
    model = UserModel

    @classmethod
    async def add_new_user(cls, new_user: UserSchema):
        async with async_session_maker() as session:
            new_user = UserModel(id=new_user.id,
                                 username=new_user.username,
                                 email=new_user.email,
                                 password=new_user.password,
                                 register_date=new_user.register_date)
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return new_user
