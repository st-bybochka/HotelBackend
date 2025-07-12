from fastapi import Depends

from app.dao.base_dao import BaseDao

from app.user.services.user_service import UserService
from app.user.user_dao import UserDao
from app.user.services.jwt_token_service import JWTTokenService
from app.user.services.hash_service import HashService
from app.user.services.login_registration_service import LoginRegistrationService
from app.user.services.login_auth_service import LoginAuthService


async def get_hash_service() -> HashService:
    return HashService()


async def get_base_dao() -> BaseDao:
    return BaseDao()


async def get_user_dao() -> UserDao:
    return UserDao()


async def get_jwt_token_service() -> JWTTokenService:
    return JWTTokenService()


async def get_login_auth_service(
        hash_service: HashService = Depends(get_hash_service),
        user_dao: UserDao = Depends(get_user_dao),
        jwt_token_service: JWTTokenService = Depends(get_jwt_token_service),
) -> LoginAuthService:
    return LoginAuthService(
        hash_service=hash_service,
        user_dao=user_dao,
        jwt_token_service=jwt_token_service,
    )


async def get_user_service(
        hash_service: HashService = Depends(get_hash_service),
        user_dao: UserDao = Depends(get_user_dao),
) -> UserService:
    return UserService(
        hash_service=hash_service,
        user_dao=user_dao,
    )


async def get_registration_service(
        hash_service: HashService = Depends(get_hash_service),
        user_dao: UserDao = Depends(get_user_dao),
) -> LoginRegistrationService:
    return LoginRegistrationService(
        hash_service=hash_service,
        user_dao=user_dao,
    )


# async def get_current_user(
#         user_dao: UserDao = Depends(CurrentUser.get_current_user),
# ) -> CurrentUser:
#     return CurrentUser(
#         user_dao=user_dao,
#     )
