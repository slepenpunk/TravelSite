from fastapi import APIRouter
from users.service import UserService
from users.schemas import UserSchema

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.get("/user/{user_id}")
async def get_user_by_id(user_id: int):
    query = await UserService.find_by_id(user_id)
    return query


@user_router.get("/get-users")
async def get_all_users() -> list[UserSchema]:
    query = await UserService.find_all()
    return query


@user_router.post("")
async def post_user(new_user: UserSchema):
    await UserService.add_new_user(new_user)
    return {"status": "OK"}
