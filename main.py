from fastapi import Depends, FastAPI, HTTPException, Request, Response
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/api/todo/", response_model=schemas.Todo)
def create_todo(request: Request, response: Response,
                todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    response.status_code = HTTP_201_CREATED
    return crud.create_todo(db=db, todo=todo)


@app.get("/api/todo/", response_model=list[schemas.Todo])
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    todos = crud.get_todos(db, skip=skip, limit=limit)
    return todos


@app.get("/api/todo/{todo_id}", response_model=schemas.Todo)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.get_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@app.put("/api/todo/{todo_id}", response_model=schemas.Todo)
def update_todo(todo_id: int, data: schemas.TodoCreate,
                db: Session = Depends(get_db)):
    db_todo = crud.update_todo(db, todo_id=todo_id, data=data)
    print("new_title: ", db_todo.title)
    if db_todo:
        return db_todo
    raise HTTPException(status_code=404, detail="Update task faild")


@app.delete("/api/todo/{todo_id}", response_model=schemas.SuccessMessage)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    is_delete = crud.delete_todo(db, todo_id=todo_id)
    if is_delete:
        return {"message": "Successfully deleted"}
    raise HTTPException(status_code=404, detail="Delete task faild")
