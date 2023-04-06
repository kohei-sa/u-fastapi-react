from pydantic import BaseModel
from typing import Optional
from decouple import config

CSRF_KEY = config("CSRF_KEY")


class CsrfSettings(BaseModel):
    secret_key: str = CSRF_KEY


class TodoBase(BaseModel):
    title: str
    description: str


class TodoCreate(TodoBase):
    pass


class Todo(TodoBase):
    id: int

    class Config:
        orm_mode = True


class SuccessMessage(BaseModel):
    message: str


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class UserLogin(UserBase):
    password: str


class User(UserBase):
    id: Optional[int]

    class Config:
        orm_mode = True


class Csrf(BaseModel):
    csrf_token: str
