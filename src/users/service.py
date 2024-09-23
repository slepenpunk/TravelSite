from users.models import UserModel
from services.base import BaseService


class UserService(BaseService):
    model = UserModel
