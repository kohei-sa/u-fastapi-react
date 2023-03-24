from sqlalchemy.orm import Session
from typing import Union

import models
import schemas


def get_todos(db: Session, skip: int = 0, limit: int = 100) -> list:
    return db.query(models.Todo).offset(skip).limit(limit).all()


def get_todo(db: Session, todo_id: int) -> Union[dict, None]:
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()


def create_todo(db: Session, todo: schemas.TodoCreate) -> dict:
    db_todo = models.Todo(
        title=todo.title, description=todo.description)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


# 更新
def update_todo(db: Session,
                todo_id: int,
                data: dict) -> Union[dict, bool]:
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    print("old_title", todo.title)
    if todo:
        todo.title = data.title
        todo.description = data.description
        db.commit()
        new_todo = db.query(models.Todo).filter(
            models.Todo.id == todo_id).first()
        return new_todo
    return False


# 削除
def delete_todo(db: Session, todo_id) -> bool:
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo:
        db.query(models.Todo).filter(models.Todo.id == todo_id).delete()
        db.commit()
        return True
    return False
