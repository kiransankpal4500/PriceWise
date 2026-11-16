from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.schemas.assistant import ChatRequest, ChatResponse
from app.ai.orchestrator import ShoppingAssistantOrchestrator

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat_with_assistant(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
):
    return await ShoppingAssistantOrchestrator.process_chat(db=db, request=request)
