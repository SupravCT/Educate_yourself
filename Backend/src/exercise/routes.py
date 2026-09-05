import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from ..database.main import get_session
from .schema import ExerciseCreateModel, ExerciseUpdateModel, ExerciseReadModel
from . import service

router = APIRouter(prefix="/exercises", tags=["exercises"])


@router.post("/", response_model=ExerciseReadModel)
async def create_exercise(data: ExerciseCreateModel, session: AsyncSession = Depends(get_session)):
    return await service.create_exercise(session, data)


@router.get("/lesson/{lesson_uid}", response_model=list[ExerciseReadModel])
async def list_exercises_for_lesson(lesson_uid: uuid.UUID, session: AsyncSession = Depends(get_session)):
    return await service.get_exercises_by_lesson(session, lesson_uid)


@router.get("/{exercise_uid}", response_model=ExerciseReadModel)
async def get_exercise(exercise_uid: uuid.UUID, session: AsyncSession = Depends(get_session)):
    exercise = await service.get_exercise(session, exercise_uid)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise


@router.patch("/{exercise_uid}", response_model=ExerciseReadModel)
async def update_exercise(exercise_uid: uuid.UUID, data: ExerciseUpdateModel, session: AsyncSession = Depends(get_session)):
    exercise = await service.update_exercise(session, exercise_uid, data)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise


@router.delete("/{exercise_uid}")
async def delete_exercise(exercise_uid: uuid.UUID, session: AsyncSession = Depends(get_session)):
    if not await service.delete_exercise(session, exercise_uid):
        raise HTTPException(status_code=404, detail="Exercise not found")
    return {"ok": True}