from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from db_dependencies import get_db

from schemas.user_schema import UserCreate, UserResponse

from services.user_service import UserService

router = APIRouter()

service = UserService()


@router.post(
        "/register",
        response_model= UserResponse
)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    new_user = service.register_user(
        db,
        user.name,
        user.email,
        user.password
    )

    return new_user