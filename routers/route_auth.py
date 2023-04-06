from fastapi import APIRouter
from fastapi import Request, Response, Depends
from fastapi_csrf_protect import CsrfProtect
from sqlalchemy.orm import Session
from schemas import UserLogin, UserCreate, User, SuccessMessage, Csrf
from user_curd import db_signup, db_login
from .get_db import get_db
from auth_utils import AuthJwtCsrf

router = APIRouter()
auth = AuthJwtCsrf()


@router.get("/api/csrftoken", response_model=Csrf)
def get_csrf_token(csrf_protect: CsrfProtect = Depends()):
    csrf_token = csrf_protect.generate_csrf()
    res = {"csrf_token": csrf_token}
    return res


@router.post("/api/register", response_model=UserCreate)
def signup(requset: Request, user: UserCreate,
           db: Session = Depends(get_db),
           csrf_protect: CsrfProtect = Depends()):
    csrf_token = csrf_protect.get_csrf_from_headers(requset.headers)
    csrf_protect.validate_csrf(csrf_token)
    new_user = db_signup(db, user)
    return new_user


@router.post("/api/login", response_model=SuccessMessage)
def login(requset: Request, response: Response,
          user: UserLogin,
          db: Session = Depends(get_db),
          csrf_protect: CsrfProtect = Depends()):
    csrf_token = csrf_protect.get_csrf_from_headers(requset.headers)
    csrf_protect.validate_csrf(csrf_token)
    token = db_login(db, user)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        samesite="none",
        secure=True
    )
    return {"message": "Successfully logged-in"}


@router.post("/api/logout", response_model=SuccessMessage)
def logout(requset: Request, response: Response,
           csrf_protect: CsrfProtect = Depends()):
    csrf_token = csrf_protect.get_csrf_from_headers(requset.headers)
    csrf_protect.vtalidate_csrf(csrf_token)
    response.set_cookie(
        key="access_token",
        value="",
        httponly=True, samesite="none", secure=True)
    return {"message": "Successfully logged-out"}


@router.get("/api/user", response_model=User)
def get_user_refresh_jwt(request: Request, response: Response):
    new_token, subject = auth.verify_update_jwt(request)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {new_token}",
        httponly=True, samesite="none", secure=True)
    return {"email": subject}
