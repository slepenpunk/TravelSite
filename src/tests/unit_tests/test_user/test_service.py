import pytest

from users.service import UserService


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "username,email,password",
    [
        ("admin", "admin@admin.com", "admin"),
        ("noexist", "noexist@noexist.com", "noexist"),
    ],
)
async def test_add_user(username, email, password):
    user = await UserService.find_one_or_none(email=email)
    if not user:
        new_user = await UserService.add(
            username=username, email=email, password=password
        )
        print(new_user)
        assert not user
        assert new_user
        assert new_user.email == email
    else:
        assert user
        assert user.email == email


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_id,email,is_exist", [(1, "admin@admin.com", True), (2, "test@test.com", True)]
)
async def test_find_user_by_id(user_id, email, is_exist):
    user = await UserService.find_by_id(user_id)
    print(user)
    if is_exist:
        assert user
        assert user.id == user_id
        assert user.email == email
    else:
        assert not user
