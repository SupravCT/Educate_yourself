from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from .model import User
from src.database.main import get_session
from .schema import UserCreateModel, UserReadModel, LoginModel, TokenModel
from . import service
from .utils import create_access_token
from ..auth.dependencies import get_current_user, require_admin
from .schema import RoleUpdateModel

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserReadModel)
async def register(data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    existing = await service.get_user_by_email(session, data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await service.create_user(session, data)


@router.post("/login", response_model=TokenModel)
async def login(data: LoginModel, session: AsyncSession = Depends(get_session)):
    user = await service.authenticate_user(session, data.email, data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    token = create_access_token(user_data={"uid": str(user.uid), "role": user.role})
    return TokenModel(access_token=token)

import uuid
from ..auth.dependencies import get_current_user, require_admin
from .schema import RoleUpdateModel

@router.get("/me", response_model=UserReadModel)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/users", response_model=list[UserReadModel])
async def list_users(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_admin),
):
    return await service.get_all_users(session)


@router.patch("/users/{user_uid}/role", response_model=UserReadModel)
async def change_user_role(
    user_uid: uuid.UUID,
    data: RoleUpdateModel,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_admin),
):
    user = await service.update_user_role(session, user_uid, data.role)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user