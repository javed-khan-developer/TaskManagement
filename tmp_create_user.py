from database import SessionLocal, Base, engine
from services.user_service import UserService
from models.chat import Chat
from models.message import Message
from models.user import User

Base.metadata.create_all(bind=engine)
db = SessionLocal()
try:
    svc = UserService()
    try:
        svc.register_user(db, 'Test User', 'test@example.com', 'password123')
        print('register_ok')
    except Exception as e:
        print('register_error', type(e).__name__, e)
finally:
    db.close()
