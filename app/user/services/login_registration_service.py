from dataclasses import dataclass

from app.user.schemas import ShemUserAuth
from app.user.services import HashService
from app.user.user_dao import UserDao

from app.exceptions import UserAlreadyExistsError, IncorrectEmailOrPasswordError


@dataclass
class LoginRegistrationService:
    hash_service: HashService
    user_dao: UserDao


    async def registration_user(self, user_data: ShemUserAuth):
        if existing_user := await self.user_dao.get_one_or_none(email=user_data.email):
            raise UserAlreadyExistsError
        hashed_password = self.hash_service.get_password_hash(user_data.password)
        await self.user_dao.add(email=user_data.email, hashed_password=hashed_password)