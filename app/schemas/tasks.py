from sqlmodel import SQLModel
from datetime import date


# READ — returned to clients
class TaskRead(SQLModel):
    id: int
    year: str
    username: str
    title: str
    creation_date: date
    task_completed: bool


# WRITE — for creating a new task
class TaskWrite(SQLModel):
    title: str
    creation_date: date
    task_completed: bool = False  # default to incomplete


# UPDATE — for PATCH requests
class TaskUpdate(SQLModel):
    task_completed: bool
