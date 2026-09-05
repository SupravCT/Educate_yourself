from sqlmodel.ext.asyncio.session import AsyncSession

from ..exercise.models import Exercise
from .rag import semantic_search
from .llm_chain import hint_chain
from .schema import HintRequestModel


async def get_hint(session: AsyncSession, data: HintRequestModel) -> str:
    exercise = await session.get(Exercise, data.exercise_uid)
    if not exercise:
        return "Exercise not found."

    retrieved_docs = semantic_search(data.user_question, k=3)
    context = "\n\n".join(doc.page_content for doc in retrieved_docs)

    user_code_block = f"User's current code:\n{data.user_code}" if data.user_code else ""

    hint = await hint_chain.ainvoke({
        "context": context,
        "exercise_prompt": exercise.prompt,
        "user_code_block": user_code_block,
        "user_question": data.user_question,
    })

    return hint