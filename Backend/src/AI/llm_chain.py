from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

from src.config import settings


SYSTEM_PROMPT = """You are a friendly coding tutor helping a student who is stuck on an exercise.
Give a helpful HINT that guides their thinking — never reveal the full solution code or write it for them.
Use the retrieved context to stay relevant to the lesson/exercise."""

hint_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", """Relevant context:
{context}

Exercise prompt: {exercise_prompt}
{user_code_block}

Student's question: {user_question}

Give a concise, encouraging hint (max 3-4 sentences). Do not write the solution."""),
])



llm = ChatGroq(
    api_key=settings.GROQ_API_KEY,
    model="openai/gpt-oss-20b",
    temperature=0.3,
)



hint_chain = hint_prompt | llm | StrOutputParser()