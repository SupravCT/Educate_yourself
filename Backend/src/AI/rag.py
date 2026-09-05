from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..lesson.models import Lesson
from ..exercise.models import Exercise

VECTOR_STORE_PATH = "faiss_index"

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)


async def load_documents(session: AsyncSession) -> list[Document]:
    
    lessons_result = await session.exec(select(Lesson))
    lessons = lessons_result.all()

    exercises_result = await session.exec(select(Exercise))
    exercises = exercises_result.all()

    documents = []

    for lesson in lessons:
        documents.append(Document(
            page_content=f"Lesson: {lesson.title}\nTopic: {lesson.topic}\nDescription: {lesson.description}",
            metadata={"type": "lesson", "uid": str(lesson.uid)},
        ))

    for exercise in exercises:
        documents.append(Document(
            page_content=f"Exercise: {exercise.title}\nPrompt: {exercise.prompt}\nStarter code: {exercise.starter_code}",
            metadata={"type": "exercise", "uid": str(exercise.uid), "lesson_uid": str(exercise.lesson_uid)},
        ))

    return documents


def split_documents(documents: list[Document]) -> list[Document]:
    
    return splitter.split_documents(documents)


def embed_and_store(chunks: list[Document]) -> FAISS:
   
    store = FAISS.from_documents(chunks, embeddings)
    store.save_local(VECTOR_STORE_PATH)
    return store


async def build_index(session: AsyncSession) -> int:
    
    documents = await load_documents(session)
    chunks = split_documents(documents)
    embed_and_store(chunks)
    return len(chunks)


def load_vectorstore() -> FAISS:
    return FAISS.load_local(
        VECTOR_STORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True,
    )


def semantic_search(query: str, k: int = 3) -> list[Document]:
    store = load_vectorstore()
    return store.similarity_search(query, k=k)