from pydantic import BaseModel
from uuid import UUID


class HintRequestModel(BaseModel):
    exercise_uid: UUID
    user_question: str
    user_code: str | None = None


class HintResponseModel(BaseModel):
    hint: str