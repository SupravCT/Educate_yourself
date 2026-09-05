import uuid
from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession

from .models import UserProgress


async def record_progress(
    session: AsyncSession,
    user_uid: uuid.UUID,
    exercise_uid: uuid.UUID,
    lesson_uid: uuid.UUID,
    xp_earned: int,
) -> UserProgress:
    # avoid duplicate XP if they solve the same exercise again
    existing = await session.exec(
        select(UserProgress).where(
            UserProgress.user_uid == user_uid,
            UserProgress.exercise_uid == exercise_uid,
        )
    )
    existing_row = existing.first()
    if existing_row:
        return existing_row

    progress = UserProgress(
        user_uid=user_uid,
        exercise_uid=exercise_uid,
        lesson_uid=lesson_uid,
        xp_earned=xp_earned,
    )
    session.add(progress)
    await session.commit()
    await session.refresh(progress)
    return progress


async def get_user_progress(session: AsyncSession, user_uid: uuid.UUID) -> list[UserProgress]:
    result = await session.exec(
        select(UserProgress).where(UserProgress.user_uid == user_uid)
    )
    return result.all()


async def get_user_stats(session: AsyncSession, user_uid: uuid.UUID) -> dict:
    result = await session.exec(
        select(
            func.coalesce(func.sum(UserProgress.xp_earned), 0),
            func.count(UserProgress.uid),
        ).where(UserProgress.user_uid == user_uid)
    )
    total_xp, exercises_completed = result.first()
    return {"total_xp": total_xp, "exercises_completed": exercises_completed}