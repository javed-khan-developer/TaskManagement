from sqlalchemy.orm import Session

from models.chat import Chat

class ChatRepository:

    def create_chat(
      self,
      db: Session,
      title: str,
      user_id: int      
    ):
        chat = Chat(
            title = title,
            user_id = user_id
            )
        
        db.add(chat)
        db.commit()
        db.refresh(chat)

        return chat
    
    def get_chat_by_id(
            self,
            db: Session,
            chat_id: int
    ):
        return (
            db.query(Chat)
            .filter(Chat.id==chat_id)
            .first()
            )
    
    def get_user_chats(
            self,
            db: Session,
            user_id: int
    ):
        
        return (
            db.query(Chat)
            .filter(Chat.user_id==user_id)
            .order_by(Chat.created_at.desc())
            .all()
        )
    
    def delete_chat(
            self,
            db: Session,
            chat: Chat
    ):
        db.delete(Chat)
        db.commit()


