import datetime

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    username: str | None = "123"
    email: str
    password: str
    register_date: datetime.datetime | None = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%dT%H:%M:%M')

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


# time_now = datetime.datetime.now(datetime.UTC)
# print(time_now)
# current_date_string = time_now.strftime('%m-%d-%yT%H:%M:%M')
# us = UserSchema(id=1,
#                 email='213',
#                 password="123")
#
# print(us.model_dump_json())
