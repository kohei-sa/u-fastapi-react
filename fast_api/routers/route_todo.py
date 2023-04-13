# タスク関係のルーター
from fastapi import APIRouter
from fastapi import Response, Request, HTTPException, Depends
from fastapi_csrf_protect import CsrfProtect
from sqlalchemy.orm import Session
import schemas
import crud
from starlette.status import HTTP_201_CREATED
from .get_db import get_db
from auth_utils import AuthJwtCsrf

router = APIRouter()
auth = AuthJwtCsrf()


@router.post("/api/todo", response_model=schemas.Todo)
def create_todo(request: Request, response: Response,
                todo: schemas.TodoCreate,
                db: Session = Depends(get_db),
                csrf_protect: CsrfProtect = Depends()):
    new_token = auth.verify_csrf_update_jwt(
        request, csrf_protect, request.headers)
    response.status_code = HTTP_201_CREATED
    response.set_cookie(
        key="access_token",
        value=f"Bearer {new_token}",
        httponly=True, samesite="none",
        secure=True)
    res = crud.create_todo(db=db, todo=todo)
    if res:
        return res
    raise HTTPException(status_code=404, detail="Create task faild")


@router.get("/api/todo", response_model=list[schemas.Todo])
def read_todos(request: Request,
               skip: int = 0, limit: int = 100,
               db: Session = Depends(get_db)):
    # auth.verify_jwt(request)
    todos = crud.get_todos(db, skip=skip, limit=limit)
    return todos


@router.get("/api/todo/{todo_id}", response_model=schemas.Todo)
def read_todo(request: Request, response: Response,
              todo_id: int,
              db: Session = Depends(get_db),
              csrf_protect: CsrfProtect = Depends()):
    new_token, _ = auth.verify_update_jwt(request)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {new_token}",
        httponly=True, samesite="none",
        secure=True)
    db_todo = crud.get_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@router.put("/api/todo/{todo_id}", response_model=schemas.Todo)
def update_todo(request: Request, response: Response,
                todo_id: int, data: schemas.TodoCreate,
                db: Session = Depends(get_db),
                csrf_protect: CsrfProtect = Depends()):
    new_token = auth.verify_csrf_update_jwt(
        request, csrf_protect, request.headers)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {new_token}",
        httponly=True, samesite="none",
        secure=True)
    db_todo = crud.update_todo(db, todo_id=todo_id, data=data)
    if db_todo:
        return db_todo
    raise HTTPException(status_code=404, detail="Update task faild")


@router.delete("/api/todo/{todo_id}", response_model=schemas.SuccessMessage)
def delete_todo(request: Request, response: Response,
                todo_id: int, db: Session = Depends(get_db),
                csrf_protect: CsrfProtect = Depends()):
    new_token = auth.verify_csrf_update_jwt(
        request, csrf_protect, request.headers)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {new_token}",
        httponly=True, samesite="none",
        secure=True)
    is_delete = crud.delete_todo(db, todo_id=todo_id)
    if is_delete:
        return {"message": "Successfully deleted"}
    raise HTTPException(status_code=404, detail="Delete task faild")
