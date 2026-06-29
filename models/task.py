from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from models.user import Base

class Task(Base):
    __tablename__="tasks"

    id= Column(Integer,primary_key=True)
    title = Column(String)
    description = Column(String)
    status = Column(String, default="Pending")
    user_id = Column(Integer, ForeignKey("users.id"))
    priority = Column(String, default="Medium")