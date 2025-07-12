from dataclasses import dataclass

from app.user.models.user_model import Users
from app.dao.base_dao import BaseDao


@dataclass
class UserDao(BaseDao):
    model = Users

    async def update_user_data(self, user_id: int, email: str, new_password: str):
        filter_by={"id": user_id}
        data = {"email": email, "hashed_password": new_password}
        await self.update(filter_by=filter_by, data=data)
