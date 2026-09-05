from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class UserProgressReadModel(BaseModel):
    uid: UUID
    exercise_uid: UUID
    lesson_uid: UUID
    xp_earned: int
    completed_at: datetime


class UserStatsModel(BaseModel):
    total_xp: int
    exercises_completed: int