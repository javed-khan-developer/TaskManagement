from sqlalchemy.orm import Session

from models.user import User


class UserRepository:

    def create_user(
        self,
        db: Session,
        name: str,
        email: str,
        password: str
    ):
        user = User(
            name=name,
            email=email,
            password=password
        )

        db.add(user)

        db.commit()

        db.refresh(user)

        return user

    def get_user_by_email(
        self,
        db: Session,
        email: str
    ):
        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )
    def get_user_by_id(
          self,
          db,
          user_id  
    ):    
        return (
            db.query(User).filter(User.id==user_id)
            .first()
            )


