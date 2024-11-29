from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import *
from app.schemas import *
from sqlalchemy import insert, select, update, delete
from slugify import slugify

ruter_task = APIRouter(prefix='/task', tags=['task'])


@ruter_task.get('/')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks


@ruter_task.get('/task_id', response_model=TaskResponse)
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalars(select(Task).where(Task.id == task_id)).first()
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


@ruter_task.post('/create')
async def create_task(db: Annotated[Session, Depends(get_db)], create_task: CreateTask, user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.execute(insert(Task).values(
        title=create_task.title,
        content=create_task.content,
        priority=create_task.priority,
        user_id=user_id
    ))
    db.commit()

    return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}

@ruter_task.put('/update')
async def update_task_1(db: Annotated[Session, Depends(get_db)], task_id: int, update_task: UpdateTask):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    db.execute(update(Task).where(Task.id == task_id).values(title=update_task.title,
                                                             content=update_task.content,
                                                             priority=update_task.priority))
    db.commit()
    return {"status_code": status.HTTP_200_OK, "transaction": "Task update is successful", }


@ruter_task.delete('/delete')
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    db.execute(delete(Task).where(Task.id == task_id))
    db.commit()
    return {"status_code": status.HTTP_200_OK, "transaction": "Task delete is successful", }
