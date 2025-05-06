from services.base import BaseService
from users.models import UserModel


class UserService(BaseService):
    model = UserModel
