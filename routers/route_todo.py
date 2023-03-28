# タスク関係のルーター
from fastapi import APIRouter, Depends
from fastapi import Response, Request, HTTPException
from sqlalchemy.orm import Session
import schemas
import crud
from starlette.status import HTTP_201_CREATED
from .get_db import get_db

router = APIRouter()


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


@router.post("/api/todo/", response_model=schemas.Todo)
def create_todo(request: Request, response: Response,
                todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    response.status_code = HTTP_201_CREATED
    return crud.create_todo(db=db, todo=todo)


@router.get("/api/todo/", response_model=list[schemas.Todo])
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    todos = crud.get_todos(db, skip=skip, limit=limit)
    return todos


@router.get("/api/todo/{todo_id}", response_model=schemas.Todo)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.get_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@router.put("/api/todo/{todo_id}", response_model=schemas.Todo)
def update_todo(todo_id: int, data: schemas.TodoCreate,
                db: Session = Depends(get_db)):
    db_todo = crud.update_todo(db, todo_id=todo_id, data=data)
    if db_todo:
        return db_todo
    raise HTTPException(status_code=404, detail="Update task faild")


@router.delete("/api/todo/{todo_id}", response_model=schemas.SuccessMessage)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    is_delete = crud.delete_todo(db, todo_id=todo_id)
    if is_delete:
        return {"message": "Successfully deleted"}
    raise HTTPException(status_code=404, detail="Delete task faild")
