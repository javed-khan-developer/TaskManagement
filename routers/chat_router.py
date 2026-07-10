from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from dependencies.database import get_db

from schemas.api_response import ApiResponse
from services.chat_service import ChatService

from schemas.chat_schema import ChatCreate
from schemas.chat_schema import MessageRequest

from dependencies.auth import get_current_user
from models.user import User

router = APIRouter(
    prefix="/chat",
    tags=["AI Chat"]
)

service = ChatService()

@router.post("/")
def create_chat(
    chat: ChatCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return service.create_chat(
        db,
        chat.title,
        current_user.id
    )

def get_user_chats(
    self,
    db: Session,
    user_id: int
):
    return self.chat_repo.get_user_chats(
        db,
        user_id
    )

@router.get("/")
def get_chats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return service.get_user_chats(
        db,
        current_user.id
    )

@router.post("/{chat_id}/message")
def send_message(
    chat_id: int,
    request: MessageRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    reply = service.send_message(
        db,
        chat_id,
        request.message
    )

    return ApiResponse(
        success=True,
        message="Message Sent",
        data=
        {
            "reply":reply
        }
    )