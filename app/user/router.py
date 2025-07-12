from fastapi import APIRouter, Response, Depends

from app.exceptions import UserAlreadyExistsError, IncorrectEmailOrPasswordError
from app.user.schemas import ShemUserAuth
from app.user.user_dao import UserDao
from app.user.auth import get_password_hash, authenticate_user, create_access_token
from app.user.user_model import Users
from app.dependencies import current_user

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"]
)


@router.post("/auth/register_v1.0")
async def register(user_data: ShemUserAuth):
    if existing_user := await UserDao.get_one_or_none(email=user_data.email):
        raise UserAlreadyExistsError
    hashed_password = get_password_hash(user_data.password)
    await UserDao.add(email=user_data.email, hashed_password=hashed_password)


@router.post("/login_v1.0")
async def login_user(response: Response, user_data: ShemUserAuth) -> str:
    user = await authenticate_user(email=user_data.email, password=user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordError
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return access_token


@router.post("/update_profile_v1.0")
async def update_profile(
        email: str,
        password: str,
        user: Users = Depends(current_user),
):
    hashed_password = get_password_hash(password)
    await UserDao.update(model_id=user.id, email=email, new_password=hashed_password)


@router.post("/logout_v1.0")
async def logout_user(response: Response):
    response.delete_cookie(key="access_token")


@router.get("/auth/me_v1.0")
async def get_user(user: Users = Depends(current_user)):
    return user
