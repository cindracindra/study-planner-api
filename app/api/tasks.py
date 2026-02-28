from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy import or_
from sqlmodel import Session, select
from starlette import status
from datetime import date

from app.dependencies.main import get_session
from app.models.tasks import Task
from app.schemas.tasks import TaskRead, TaskWrite, TaskUpdate


task_router = APIRouter(
    prefix="/{year}/{username}/personal-tasks",
    tags=["personal tasks"],
)


@task_router.get("", response_model=list[TaskRead])
def get_personal_tasks(
    year: str = Path(..., description="Academic year in short form e.g. 2324"),
    username: str = Path(..., description="Username"),
    session: Session = Depends(get_session),
):
    query = select(Task).where(
        Task.year == year,
        Task.username == username,
        or_(Task.creation_date == date.today(), Task.task_completed == False),
    )
    return session.exec(query).all()


@task_router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_personal_task(
    task: TaskWrite,
    year: str = Path(..., description="Academic year in short form e.g. 2324"),
    username: str = Path(..., description="Username"),
    session: Session = Depends(get_session),
):
    new_task = Task(
        username=username,
        year=year,
        title=task.title,
        creation_date=task.creation_date,
    )
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task


@task_router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int,
    session: Session = Depends(get_session),
):
    query = select(Task).where(Task.id == task_id)
    task = session.exec(query).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )
    return task


@task_router.patch(
    "/{task_id}", response_model=TaskRead, status_code=status.HTTP_200_OK
)
def update_task_completion(
    task_id: int,
    patch: TaskUpdate,
    session: Session = Depends(get_session),
):
    query = select(Task).where(Task.id == task_id)
    task = session.exec(query).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )
    task.task_completed = patch.task_completed
    session.commit()
    session.refresh(task)
    return task


@task_router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    year: str = Path(..., description="Academic year in short form e.g. 2324"),
    username: str = Path(..., description="Username"),
    session: Session = Depends(get_session),
):
    query = select(Task).where(
        Task.id == task_id,
        Task.year == year,
        Task.username == username,
    )
    task = session.exec(query).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )
    session.delete(task)
    session.commit()
    return None
