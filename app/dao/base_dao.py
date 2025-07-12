from sqlalchemy import select, insert, update, delete
from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session_maker


@dataclass
class BaseDao:
    model = None

    async def get_all(self, **filter_by):
        async with async_session_maker() as session:
            query = select(self.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        async with async_session_maker() as session:
            query = select(self.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def get_by_id(self, model_id: int):
        async with async_session_maker() as session:
            query = select(self.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def add(self, **model_data):
        async with async_session_maker() as session:
            query = insert(self.model).values(**model_data)
            await session.execute(query)
            await session.commit()

    async def update(self, filter_by: dict, data: dict):
        async with async_session_maker() as session:
            query = update(self.model).filter_by(**filter_by).values(**data)
            await session.execute(query)
            await session.commit()
