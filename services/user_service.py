from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi import status
from repositories.user_repository import UserRepository
from schemas.api_response import ApiResponse
from utils.security import hash_password
from utils.security import verify_password
from utils.jwt_helper import create_access_token
from utils.logger import logger

class UserService:

    def __init__(self):
        self.repo = UserRepository()

    def register_user(
        self,
        db: Session,
        name: str,
        email: str,
        password: str
    ):
        existing_user = self.repo.get_user_by_email(
            db,
            email
        )

        if existing_user:
            raise HTTPException(
               status_code= status.HTTP_409_CONFLICT,detail= "Email already exists"
            )
        hashed_password = hash_password(password)

        logger.info(f"HASH:, {hashed_password}")  

        return self.repo.create_user(
            db,
            name,
            email,
            hashed_password
        )
    
    def login_user(
    self,
    db,
    email,
    password
        ):
        user = self.repo.get_user_by_email(
        db,
        email
    )

        if not user:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials"
        )

        valid = verify_password(
        password,
        user.password
        )

        if not valid:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials"
        )

        token = create_access_token(
        {
            "user_id": user.id,
            "email": user.email
        }
        )   
        return ApiResponse(
            success=True,
            message="Login Successfull",
            data= token
        )