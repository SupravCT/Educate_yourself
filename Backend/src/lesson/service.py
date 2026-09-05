import uuid
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .models import Lesson
from .schema import LessonCreateModel, LessonUpdateModel


async def create_lesson(session: AsyncSession, data: LessonCreateModel) -> Lesson:
    lesson = Lesson(**data.model_dump())
    session.add(lesson)
    await session.commit()
    await session.refresh(lesson)
    return lesson


async def get_lesson(session: AsyncSession, lesson_uid: uuid.UUID) -> Lesson | None:
    return await session.get(Lesson, lesson_uid)


async def get_all_lessons(session: AsyncSession) -> list[Lesson]:
    statement = select(Lesson).order_by(Lesson.order_index)
    result = await session.exec(statement)
    return result.all()


async def update_lesson(session: AsyncSession, lesson_uid: uuid.UUID, data: LessonUpdateModel) -> Lesson | None:
    lesson = await session.get(session, lesson_uid)
    if not lesson:
        return None
    for key, value in data.model_dump().items():
        setattr(lesson, key, value)
    session.add(lesson)
    await session.commit()
    await session.refresh(lesson)
    return lesson


async def delete_lesson(session: AsyncSession, lesson_uid: uuid.UUID) -> bool:
    lesson = await session.get(Lesson, lesson_uid)
    if not lesson:
        return False
    await session.delete(lesson)
    await session.commit()
    return True