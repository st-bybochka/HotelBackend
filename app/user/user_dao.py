from sqlalchemy import update
from app.database import async_session_maker

from app.user.user_model import Users
from app.dao.base_dao import BaseDao


class UserDao(BaseDao):
    model = Users

    @classmethod
    async def update(cls, model_id, email: str, new_password: str):
        async with async_session_maker() as session:
            query = update(cls.model).values(email=email, hashed_password=new_password).filter_by(id=model_id)
            await session.execute(query)
            await session.commit()


