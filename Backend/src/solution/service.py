import uuid
from sqlmodel.ext.asyncio.session import AsyncSession

from .models import Submission
from .schema import SubmissionCreateModel
from .sandbox import run_code
from ..exercise.models import Exercise
from ..progress.service import record_progress
from .schema import RunCodeModel

def normalize(output: str) -> str:
    lines = output.strip().splitlines()
    stripped_lines = [line.strip() for line in lines]
    return "\n".join(stripped_lines)


async def check_submission(session: AsyncSession, data: SubmissionCreateModel, user_uid: uuid.UUID) -> Submission | None:
    exercise = await session.get(Exercise, data.exercise_uid)
    if not exercise:
        return None

    full_code = f"{data.submitted_code}\n\n{exercise.test_code}"

    result = await run_code(full_code)
    run_result = result.get("run", {})
    actual_output = normalize(run_result.get("stdout") or "")
    stderr = run_result.get("stderr")

    expected = normalize(exercise.expected_output)
    is_correct = actual_output == expected and not stderr

    xp_awarded = exercise.xp_reward if is_correct else 0

    submission = Submission(
        exercise_uid=data.exercise_uid,
        user_uid=user_uid,
        submitted_code=data.submitted_code,
        is_correct=is_correct,
        xp_awarded=xp_awarded,
    )
    session.add(submission)
    await session.commit()
    await session.refresh(submission)

    if is_correct:
        await record_progress(
            session,
            user_uid=user_uid,
            exercise_uid=exercise.uid,
            lesson_uid=exercise.lesson_uid,
            xp_earned=xp_awarded,
        )

    return submission

async def run_user_code(session: AsyncSession, data: RunCodeModel) -> dict:
    exercise = await session.get(Exercise, data.exercise_uid)
    if not exercise:
        return {"stdout": "", "stderr": "Exercise not found"}

    full_code = f"{data.submitted_code}\n\n{exercise.test_code}"
    result = await run_code(full_code)
    run_result = result.get("run", {})

    return {
        "stdout": run_result.get("stdout") or "",
        "stderr": run_result.get("stderr") or None,
    }