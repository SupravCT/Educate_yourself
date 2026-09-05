import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class Lesson(SQLModel, table=True):
    __tablename__ = "lessons"

    uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    title: str
    description: str
    topic: str
    order_index: int
    difficulty: str
    xp_reward: int = Field(default=10)

    created_at: datetime = Field(default_factory=datetime.utcnow)