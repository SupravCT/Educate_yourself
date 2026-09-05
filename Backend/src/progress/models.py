import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field


class UserProgress(SQLModel, table=True):
    __tablename__ = "user_progress"

    uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_uid: uuid.UUID = Field(foreign_key="users.uid")
    exercise_uid: uuid.UUID = Field(foreign_key="exercises.uid")
    lesson_uid: uuid.UUID = Field(foreign_key="lessons.uid")

    xp_earned: int = Field(default=0)
    completed_at: datetime = Field(default_factory=datetime.utcnow)