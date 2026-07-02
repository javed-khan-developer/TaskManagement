from fastapi import APIRouter
from schemas.chat_schema import ChatRequest
from schemas.chat_schema import ChatResponse

from services.ai_service import AiService

router= APIRouter()
service = AiService()

@router.post(
    "/chat",
    response_model=ChatResponse
    )

def chat(
    request: ChatRequest
):
    reply = service.chat(
        request.message
    )

    return ChatResponse(
        reply=reply
    )