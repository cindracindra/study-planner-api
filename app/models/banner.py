from datetime import date
from sqlmodel import SQLModel, Field
from typing import Optional


class Banner(SQLModel, table=True):
    __tablename__ = "banner"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    year: str = Field(index=True)
    date: date
    banner_type: str
    display_text: str 
