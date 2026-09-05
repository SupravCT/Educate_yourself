from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ExerciseCreateModel(BaseModel):
    lesson_uid: UUID
    title: str
    prompt: str
    starter_code: str
    solution_code: str
    test_code: str
    expected_output: str
    order_index: int
    xp_reward: int = 5
    difficulty: str


class ExerciseUpdateModel(BaseModel):
    title: str | None = None
    prompt: str | None = None
    starter_code: str | None = None
    solution_code: str | None = None
    test_code: str | None = None
    expected_output: str | None = None
    order_index: int | None = None
    xp_reward: int | None = None
    difficulty: str | None = None


class ExerciseReadModel(BaseModel):
    uid: UUID
    lesson_uid: UUID
    title: str
    prompt: str
    starter_code: str
    test_code: str
    order_index: int
    xp_reward: int
    difficulty: str
    created_at: datetime
    
   