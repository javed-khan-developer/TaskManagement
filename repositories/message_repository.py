from sqlalchemy.orm import Session

from models.message import Message

class MessageRepository:

    def create_message(
            self,
            db:Session,
            chat_id: int,
            role: str,
            content: str
    ): 
        message = Message(
            chat_id=chat_id,
            role=role,
            content = content
            )
        
        db.add(message)
        db.commit()
        db.refresh()

        return message
    
    def get_chat_messages(
        self,
        db: Session,
        chat_id: int
        ):

        return(
            db.query(Message)
               .filter(Message.chat_id==chat_id)
               .order_by(Message.created_at.asc())
               .all()
               )
    
    def delete_chat_messages(
       self,
        db: Session,
        chat_id: int     
    ):
        (
            db.query(Message).
            filter(Message.chat_id==chat_id).delete()
        )

        db.commit()