from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime

from datetime import datetime

from models.user import Base


class Message(Base):
    __tablename__="message"

    id = Column(
        Integer,
        primary_key= True
    )

    chat_id = Column(
        Integer,
        ForeignKey("chats.id")
    )

    role = Column(
        Text
    )

    content= Column(
        Text
    )

    created_at = Column(
        DateTime,
        default= datetime.utcnow
    )