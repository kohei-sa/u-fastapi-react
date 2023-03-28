from fastapi import HTTPException
from sqlalchemy.orm import Session
from auth_utils import AuthJwtCsrf
import models
import schemas

auth = AuthJwtCsrf()


def db_signup(db: Session, user: schemas.UserCreate) -> dict:
    email = user.email
    password = user.password
    overlap_user = db.query(models.User).filter(
        models.User.email == email).first()
    if overlap_user:
        raise HTTPException(status_code=400, detail="Email is already taken")
    if not password or len(password) < 6:
        raise HTTPException(status_code=400, detail="Password too short")
    db_user = models.User(
        email=email, password=auth.generate_hashed_pw(password))
    db.add(db_user)
    db.commit()

    db_new_user = db.query(models.User).filter(
        models.User.email == db_user.email).first()
    return db_new_user


def db_login(db: Session, user: schemas.UserLogin) -> str:
    email = user.email
    password = user.password
    user = db.query(models.User).filter(
        models.User.email == email).first()
    if not user or not auth.verify_pw(password, user.password):
        raise HTTPException(
            status_code=401, detail="Invalid email or password")
    token = auth.encode_jwt(user.email)
    return token
