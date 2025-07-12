from pydantic import BaseModel, EmailStr


class ShemUserAuth(BaseModel):
    email: EmailStr
    password: str
