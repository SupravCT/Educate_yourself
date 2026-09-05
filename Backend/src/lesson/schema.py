from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class LessonCreateModel(BaseModel):
    title: str
    description: str
    topic: str
    order_index: int
    difficulty: str
    xp_reward: int = 10


class LessonUpdateModel(BaseModel):
    title: str | None = None
    description: str | None = None
    topic: str | None = None
    order_index: int | None = None
    difficulty: str | None = None
    xp_reward: int | None = None


class LessonReadModel(BaseModel):
    uid: UUID
    title: str
    description: str
    topic: str
    order_index: int
    difficulty: str
    xp_reward: int
    created_at: datetime