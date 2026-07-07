from database import SessionLocal
from repositories.user_repository import UserRepository
from utils.security import hash_password

db = SessionLocal()
try:
    repo = UserRepository()
    user = repo.get_user_by_email(db, 'test@example.com')
    if user:
        user.password = hash_password('password123')
        db.commit()
        print('password_updated')
    else:
        print('user_not_found')
finally:
    db.close()
