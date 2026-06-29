from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from dependencies import get_db
from schemas.login_schema import LoginRequest
from services.user_service import UserService
from auth_dependency import get_current_user


router = APIRouter()
service = UserService()

@router.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    try:
        token = service.login_user(
            db,
            request.email,
            request.password
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=401,
            detail=str(exc)
        )

    return {
        "access_token": token
    }

@router.get("/me")
def me(
    current_user= Depends(get_current_user)
    ):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email
    }