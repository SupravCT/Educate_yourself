import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field


class Submission(SQLModel, table=True):
    __tablename__ = "submissions"

    uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    exercise_uid: uuid.UUID = Field(foreign_key="exercises.uid")
    user_uid: uuid.UUID = Field(foreign_key="users.uid")

    submitted_code: str
    is_correct: bool
    xp_awarded: int = Field(default=0)

    created_at: datetime = Field(default_factory=datetime.utcnow)