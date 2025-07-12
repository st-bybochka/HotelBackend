from fastapi import Response
from pydantic import EmailStr
from dataclasses import dataclass

from app.user.services.hash_service import HashService
from app.user.services.jwt_token_service import JWTTokenService
from app.user.user_dao import UserDao
from app.exceptions import UserAlreadyExistsError, IncorrectEmailOrPasswordError
from app.user.schemas import ShemUserAuth

@dataclass
class LoginAuthService:
    hash_service: HashService
    user_dao: UserDao
    jwt_token_service: JWTTokenService


    async def login(self, response: Response, user_data: ShemUserAuth):
        user = await self._authenticate_user(email=user_data.email, password=user_data.password)
        if not user:
            raise IncorrectEmailOrPasswordError
        access_token = self.jwt_token_service.create_access_token({"sub": str(user.id)})
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        return access_token

    async def _authenticate_user(self, email: EmailStr, password: str):
        user = await self.user_dao.get_one_or_none(email=email)
        if not user and self.hash_service.verify_password(plain_password=password, hashed_password=user.hashed_password):
            return None
        return user