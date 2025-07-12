from fastapi import APIRouter, Response, Depends

from app.DI import (get_registration_service,
                    get_login_auth_service,
                    get_user_service)

from app.user.schemas import ShemUserAuth
from app.user.services.login_registration_service import LoginRegistrationService
from app.user.services.login_auth_service import LoginAuthService
from app.user.services.user_service import UserService
from app.user.models.user_model import Users
from app.user.dependencies import current_user

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"]
)


@router.post("/auth/register_v1.0")
async def register(
        user_data: ShemUserAuth,
        login_registration_service: LoginRegistrationService = Depends(get_registration_service),
):
    await login_registration_service.registration_user(user_data=user_data)


@router.post("/login_v1.0")
async def login_user(
        response: Response,
        user_data: ShemUserAuth,
        login_auth_service: LoginAuthService = Depends(get_login_auth_service)
) -> str:
    return await login_auth_service.login(response=response, user_data=user_data)


@router.post("/update_profile_v1.0")
async def update_profile(
        email: str,
        password: str,
        user: Users = Depends(current_user),
        user_service: UserService = Depends(get_user_service)
):
    await user_service.update_user(user_id=user.id, email=email, password=password)


@router.post("/logout_v1.0")
async def logout_user(response: Response):
    response.delete_cookie(key="access_token")


@router.get("/auth/me_v1.0")
async def get_user(
        user: Users = Depends(current_user)):
    return user
