'''from langchain_core.documents import Document
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
    return store.similarity_search(query, k=k)'''


from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings
from fastembed import TextEmbedding
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..lesson.models import Lesson
from ..exercise.models import Exercise

VECTOR_STORE_PATH = "faiss_index"


class FastEmbedWrapper(Embeddings):
    def __init__(self):
        self.model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [vec.tolist() for vec in self.model.embed(texts)]

    def embed_query(self, text: str) -> list[float]:
        return list(self.model.embed([text]))[0].tolist()


embeddings = FastEmbedWrapper()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)


async def load_documents(session: AsyncSession) -> list[Document]:
    """Step 1: LOAD — pull lessons + exercises from DB instead of a PDF."""
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
        # solution_code and expected_output intentionally excluded — hints shouldn't leak the answer
        documents.append(Document(
            page_content=f"Exercise: {exercise.title}\nPrompt: {exercise.prompt}\nStarter code: {exercise.starter_code}",
            metadata={"type": "exercise", "uid": str(exercise.uid), "lesson_uid": str(exercise.lesson_uid)},
        ))

    return documents


def split_documents(documents: list[Document]) -> list[Document]:
    """Step 2: SPLIT — recursive character splitting."""
    return splitter.split_documents(documents)


def embed_and_store(chunks: list[Document]) -> FAISS:
    """Step 3 + 4: EMBED the chunks, STORE them in a FAISS vector store."""
    store = FAISS.from_documents(chunks, embeddings)
    store.save_local(VECTOR_STORE_PATH)
    return store


async def build_index(session: AsyncSession) -> int:
    """Full pipeline: load -> split -> embed -> store."""
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
    """Retrieve the top-k most relevant chunks for a query."""
    store = load_vectorstore()
    return store.similarity_search(query, k=k)