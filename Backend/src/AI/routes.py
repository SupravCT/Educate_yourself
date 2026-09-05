from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from ..database.main import get_session
from .schema import HintRequestModel, HintResponseModel
from .rag import build_index
from . import service

router = APIRouter(prefix="/hints", tags=["hints"])


@router.post("/", response_model=HintResponseModel)
async def get_hint(data: HintRequestModel, session: AsyncSession = Depends(get_session)):
    hint = await service.get_hint(session, data)
    return HintResponseModel(hint=hint)


@router.post("/reindex")
async def reindex(session: AsyncSession = Depends(get_session)):
    count = await build_index(session)
    return {"indexed_documents": count}