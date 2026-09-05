import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field


class Exercise(SQLModel, table=True):
    __tablename__ = "exercises"

    uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    lesson_uid: uuid.UUID = Field(foreign_key="lessons.uid")

    title: str
    prompt: str
    starter_code: str
    solution_code: str
    test_code: str
    expected_output: str
    order_index: int
    xp_reward: int = Field(default=5)
    difficulty: str

    created_at: datetime = Field(default_factory=datetime.utcnow)