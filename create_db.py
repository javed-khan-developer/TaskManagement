
# create_db.py

from core.database import engine
from models.user import Base
from models.task import Task

Base.metadata.create_all(bind=engine)