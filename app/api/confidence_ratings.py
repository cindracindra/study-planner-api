from fastapi import APIRouter, Depends, Path, Query, HTTPException
from sqlalchemy import or_
from sqlmodel import Session, select
from starlette import status

from app.dependencies.main import get_session
from app.models.confidence_ratings import ConfidenceRating, ModuleRating
from app.schemas.confidence_ratings import (
    ConfidenceRatingRead,
    ModuleRatingRead,
    ModuleRatingUpdate,
)


task_router = APIRouter(
    prefix="/{year}/{username}/personal-confidence-ratings",
    tags=["personal confidence ratings"],
)


@task_router.get("", response_model=ConfidenceRatingRead)
def get_personal_confidence_ratings(
    module_codes: list[str] | None = Query(
        None, alias="module_code"
    ),  # ← List from query params
    year: str = Path(..., description="Academic year in short form e.g. 2324"),
    username: str = Path(..., description="Username"),
    session: Session = Depends(get_session),
):
    query = select(ConfidenceRating).where(
        ConfidenceRating.year == year,
        ConfidenceRating.username == username,
    )

    if module_codes:
        query = query.where(
            ConfidenceRating.module_ratings.any(
                ModuleRating.module_code.in_(module_codes)
            )
        )

    result = session.exec(query).first()
    if not result:
        raise HTTPException(status_code=404, detail="Confidence rating not found")
    return result


@task_router.patch(
    "/modules/{module_rating_id}",
    response_model=ModuleRatingRead,
    status_code=status.HTTP_200_OK,
)
def update_module_rating(
    rating_update: ModuleRatingUpdate,
    module_rating_id: int = Path(..., description="ID of the module rating to update"),
    session: Session = Depends(get_session),
):
    query = select(ModuleRating).where(ModuleRating.id == module_rating_id)
    module_rating = session.exec(query).first()
    if not module_rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module rating not found.",
        )

    module_rating.rating = rating_update.rating
    session.commit()
    session.refresh(module_rating)
    return module_rating
