from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


class ModuleRating(SQLModel, table=True):
    __tablename__ = "module_ratings"

    id: Optional[int] = Field(default=None, primary_key=True)
    module_code: str
    rating: Optional[int] = None
    term_week: int

    # Foreign key to parent
    confidence_rating_id: int = Field(foreign_key="confidence_ratings.id")
    confidence_rating: "ConfidenceRating" = Relationship(
        back_populates="module_ratings"
    )


class ConfidenceRating(SQLModel, table=True):
    __tablename__ = "confidence_ratings"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    year: str = Field(index=True)

    # One-to-many relationship
    module_ratings: list["ModuleRating"] = Relationship(
        back_populates="confidence_rating",
        sa_relationship_kwargs={"lazy": "selectin", "passive_deletes": True},
    )
