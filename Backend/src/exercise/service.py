import uuid
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .models import Exercise
from .schema import ExerciseCreateModel, ExerciseUpdateModel


async def create_exercise(session: AsyncSession, data: ExerciseCreateModel) -> Exercise:
    exercise = Exercise(**data.model_dump())
    session.add(exercise)
    await session.commit()
    await session.refresh(exercise)
    return exercise


async def get_exercise(session: AsyncSession, exercise_uid: uuid.UUID) -> Exercise | None:
    return await session.get(Exercise, exercise_uid)


async def get_exercises_by_lesson(session: AsyncSession, lesson_uid: uuid.UUID) -> list[Exercise]:
    statement = (
        select(Exercise)
        .where(Exercise.lesson_uid == lesson_uid)
        .order_by(Exercise.order_index)
    )
    result = await session.exec(statement)
    return result.all()


async def update_exercise(session: AsyncSession, exercise_uid: uuid.UUID, data: ExerciseUpdateModel) -> Exercise | None:
    exercise = await session.get(Exercise, exercise_uid)
    if not exercise:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(exercise, key, value)
    session.add(exercise)
    await session.commit()
    await session.refresh(exercise)
    return exercise


async def delete_exercise(session: AsyncSession, exercise_uid: uuid.UUID) -> bool:
    exercise = await session.get(Exercise, exercise_uid)
    if not exercise:
        return False
    await session.delete(exercise)
    await session.commit()
    return True