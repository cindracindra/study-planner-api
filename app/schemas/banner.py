from datetime import date
from sqlmodel import SQLModel
from typing import Literal, Optional


class BannerRead(SQLModel):
    id: int
    year: str
    username: str
    date: date
    banner_type: str
    display_text: str


class BannerWrite(SQLModel):
    banner_type: Literal["quote", "excuse", "custom"]
    display_text: Optional[str] = None
