from sqlmodel import SQLModel, Field
from datetime import date
from typing import Optional


class Task(SQLModel, table=True):
    __tablename__ = "personal_tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    year: str = Field(index=True) 
    username: str = Field(index=True)
    title: str
    creation_date: date = Field(default_factory=date.today)
    task_completed: bool = Field(default=False)
