from fastapi import APIRouter, Depends
from fastapi import Response
from sqlalchemy.orm import Session
from schemas import UserLogin, UserCreate, SuccessMessage
from user_curd import db_signup, db_login
from .get_db import get_db
from auth_utils import AuthJwtCsrf

router = APIRouter()
auth = AuthJwtCsrf()


@router.post("/api/register", response_model=UserCreate)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    new_user = db_signup(db, user)
    return new_user


@router.post("/api/login", response_model=SuccessMessage)
def login(response: Response, user: UserLogin, db: Session = Depends(get_db)):
    token = db_login(db, user)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        samesite="none",
        secure=True
    )
    return {"message": "Successfully logged-in"}
