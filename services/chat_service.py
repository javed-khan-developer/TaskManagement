from sqlalchemy.orm import Session

from repositories.chat_repository import ChatRepository
from repositories.message_repository import MessageRepository
from services.ai_service import AiService

class ChatService:
    def __init__(self):
        self.chat_repo= ChatRepository()
        self.message_repo= MessageRepository()
        self.ai_service= AiService()

        def create_chat(
                self,
                db: Session,
                title: str,
                user_id: str
        ):
            return self.chat_repo.create_chat(
                db,
                title,
                user_id
            )
        
        def send_message(
          self,
          db: Session,
          chat_id: int,
          message: str
        ):
            self.message_repo.create_message(
                db= db,
                chat_id=chat_id,
                role="user",
                content= message
            )

            messages = self.message_repo_get_chat_messages(
                db,
                chat_id
            )

            gemini_messages = []

            for msg in messages:
                role = (
                    "model"
                    if msg.role=="assistant"
                    else "user"
                    )
                
                gemini_messages.append({
                    "role": role,
                    "parts": [
                        {
                            "text": msg.content
                        }
                    ]
                })

                reply = self.ai_service_chat(
                    gemini_messages
                )

                self.message_repo.create_message(
                db= db,
                chat_id=chat_id,
                role="assistant",
                content= reply
                )

                return reply
            
            

            

        






