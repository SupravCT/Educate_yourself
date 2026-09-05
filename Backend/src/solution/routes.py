from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from src.database.main import get_session
from ..auth.dependencies import get_current_user
from ..auth.model import User
from .schema import SubmissionCreateModel, SubmissionResultModel
from . import service
from .schema import RunCodeModel, RunResultModel

router = APIRouter(prefix="/submissions", tags=["submissions"])


@router.post("/", response_model=SubmissionResultModel)
async def submit_solution(
    data: SubmissionCreateModel,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    submission = await service.check_submission(session, data, current_user.uid)
    if not submission:
        raise HTTPException(status_code=404, detail="Exercise not found")

    return SubmissionResultModel(
        uid=submission.uid,
        exercise_uid=submission.exercise_uid,
        is_correct=submission.is_correct,
        xp_awarded=submission.xp_awarded,
        message="Correct!" if submission.is_correct else "Not quite, try again.",
        created_at=submission.created_at,
    )


@router.post("/run", response_model=RunResultModel)
async def run_solution(
    data: RunCodeModel,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    result = await service.run_user_code(session, data)
    return RunResultModel(**result)