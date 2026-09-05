from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class SubmissionCreateModel(BaseModel):
    exercise_uid: UUID
    submitted_code: str


class SubmissionResultModel(BaseModel):
    uid: UUID
    exercise_uid: UUID
    is_correct: bool
    xp_awarded: int
    message: str
    created_at: datetime

class RunCodeModel(BaseModel):
    exercise_uid: UUID
    submitted_code: str


class RunResultModel(BaseModel):
    stdout: str
    stderr: str | None = None