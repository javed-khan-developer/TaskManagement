from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime

from datetime import datetime

from models.user import Base

class Chat(Base):
    __tablename__="chats"

    id = Column(
        Integer,
        primary_key=True
    )

    title = Column(
        String
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    created_at = Column(
        DateTime,
        default= datetime.utcnow
    )

