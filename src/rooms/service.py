from rooms.models import RoomModel
from services.base import BaseService


class RoomService(BaseService):
    model = RoomModel
