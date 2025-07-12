from fastapi import Request, Depends
from jose import jwt, JWTError
from datetime import datetime


from app.exceptions import TokenExpiredError, TokenAbsentError, TokenIncorrectError
from app.user.user_dao import UserDao
from app.config import settings


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise TokenAbsentError
    return token


async def current_user(token: str = Depends(get_token)):

    try:
        payload = jwt.decode(
            token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except JWTError:
        raise TokenIncorrectError

    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredError

    user_id: str = payload.get("sub")
    if not user_id:
        raise TokenIncorrectError

    user_dao = UserDao()
    user = await user_dao.get_by_id(model_id=int(user_id))
    if not user:
        raise TokenIncorrectError

    return user
