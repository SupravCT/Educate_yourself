import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..auth.dependencies import require_admin
from src.database.main import get_session

from .schema import LessonCreateModel, LessonUpdateModel, LessonReadModel
from . import service

router = APIRouter(prefix="/lessons", tags=["lessons"])


@router.post("/", response_model=LessonReadModel)
async def create_lesson(data: LessonCreateModel,
                         session: Session = Depends(get_session),
                         current_user=Depends(require_admin)):
    return await service.create_lesson(session, data)


@router.get("/", response_model=list[LessonReadModel])
async def list_lessons(session: Session = Depends(get_session)):
    return await service.get_all_lessons(session)


@router.get("/{lesson_uid}", response_model=LessonReadModel)
async def get_lesson(lesson_uid: uuid.UUID, session: Session = Depends(get_session)):
    lesson = await service.get_lesson(session, lesson_uid)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


@router.patch("/{lesson_uid}", response_model=LessonReadModel)
async def update_lesson(lesson_uid: uuid.UUID, data: LessonUpdateModel, session: Session = Depends(get_session)):
    lesson = await service.update_lesson(session, lesson_uid, data)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


@router.delete("/{lesson_uid}")
async def delete_lesson(lesson_uid: uuid.UUID, session: Session = Depends(get_session)):
    if not await service.delete_lesson(session, lesson_uid):
        raise HTTPException(status_code=404, detail="Lesson not found")
    return {"ok": True}