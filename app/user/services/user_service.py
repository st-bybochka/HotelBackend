from dataclasses import dataclass

from app.user.services import HashService
from app.user.user_dao import UserDao


@dataclass
class UserService:
    hash_service: HashService
    user_dao: UserDao

    async def update_user(self, user_id: int, email: str, password: str):
        hashed_password = self.hash_service.get_password_hash(password)
        await self.user_dao.update_user_data(user_id=user_id, email=email, new_password=hashed_password)