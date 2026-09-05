from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime


class UserCreateModel(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserReadModel(BaseModel):
    uid: UUID
    username: str
    email: str
    role: str
    xp: int
    created_at: datetime


class LoginModel(BaseModel):
    email: EmailStr
    password: str


class TokenModel(BaseModel):
    access_token: str
    token_type: str = "bearer"

class RoleUpdateModel(BaseModel):
    role: str 