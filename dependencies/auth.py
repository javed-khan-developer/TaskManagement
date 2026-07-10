from fastapi import Depends
from fastapi import HTTPException

from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials

from sqlalchemy.orm import Session

from dependencies.database import get_db

from repositories.user_repository import UserRepository

from utils.jwt_helper import verify_token


security = HTTPBearer()

def get_current_user(
        credentials: HTTPAuthorizationCredentials= Depends(security),
        db: Session = Depends(get_db)

):
    token= credentials.credentials
    payload= verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401,detail='Invalid Token')
    user_id=payload.get("user_id")
    repo= UserRepository()
    user= repo.get_user_by_id(db,user_id)

    if user is None:
        raise HTTPException(status_code=401,detail="User Not Found")
    
    return user


