from rooms.models import RoomModel
from services.base import BaseService
from database import async_session_maker


class RoomService(BaseService):
    model = RoomModel
