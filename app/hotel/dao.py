from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import async_session_maker
from app.hotel.schemas import HotelsModel
from app.hotel.hotel_model import Hotels


class HotelService:

    @classmethod
    async def get_available_rooms(cls, location: str):
        async with async_session_maker() as session:
            stmt = (
                select(Hotels)
                .where(Hotels.location.like(f"%{location}%"))
                .options(selectinload(Hotels.rooms))
            )
            result = await session.execute(stmt)
            hotels = result.scalars().unique().all()
            return hotels

    @classmethod
    async def get_hotels_by_stars(cls) -> list[HotelsModel]:
        async with async_session_maker() as session:
            query = select(Hotels)
            result = await session.execute(query)
            return result.scalars().all()
