from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.database.main import get_session
from ..auth.dependencies import get_current_user
from ..auth.model import User
from .schema import UserProgressReadModel, UserStatsModel
from . import service

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("/me", response_model=list[UserProgressReadModel])
async def my_progress(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await service.get_user_progress(session, current_user.uid)


@router.get("/me/stats", response_model=UserStatsModel)
async def my_stats(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await service.get_user_stats(session, current_user.uid)