from sqlalchemy import select, insert, delete
from database import async_session_maker


class BaseService:
    model = None

    # READ
    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **data):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**data)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    # CREATE
    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(**data).returning(cls.model)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one_or_none()

    # DELETE
    @classmethod
    async def delete(cls, **item_id):
        async with async_session_maker() as session:
            exists_item = await cls.find_one_or_none(**item_id)
            if exists_item is None:
                return None
            stmt = delete(cls.model).filter_by(**item_id)
            await session.execute(stmt)
            await session.commit()
            return exists_item

    # UPDATE
