from sqlmodel import SQLModel
from typing import Optional


class ModuleRatingRead(SQLModel):
    id: int
    module_code: str
    rating: Optional[int]
    term_week: int


class ModuleRatingWrite(SQLModel):
    module_code: str
    rating: Optional[int] = None
    term_week: int


class ModuleRatingUpdate(SQLModel):
    rating: int


class ConfidenceRatingRead(SQLModel):
    id: int
    year: str
    username: str
    module_ratings: list[ModuleRatingRead] = []


class ConfidenceRatingWrite(SQLModel):
    module_ratings: list[ModuleRatingWrite] = []
