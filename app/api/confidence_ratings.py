from fastapi import APIRouter, Depends, Path, Query, HTTPException
from sqlalchemy import or_
from sqlmodel import Session, select
from starlette import status

from app.dependencies.main import get_current_user, get_session
from app.models.confidence_ratings import ConfidenceRating, ModuleRating
from app.schemas.confidence_ratings import (
    ConfidenceRatingRead,
    ModuleRatingRead,
    ModuleRatingUpdate,
)
from app.utils.sync_helpers import get_sync_status, needs_sync, update_sync_status, create_missing_ratings


confidence_ratings_router = APIRouter(
    prefix="/me/{year}/personal-confidence-ratings",
    tags=["personal confidence ratings"],
)


@confidence_ratings_router.get("", response_model=ConfidenceRatingRead)
def get_personal_confidence_ratings(
    module_codes: list[str] | None = Query(
        None, alias="module_code"
    ),
    year: str = Path(..., description="Academic year in short form e.g. 2324"),
    username: str = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    sync_status = get_sync_status(session, year, username)
    if needs_sync(sync_status):
        create_missing_ratings(session, year, username, total_weeks=11)
        update_sync_status(session, year, username)

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


@confidence_ratings_router.patch(
    "/modules/{module_rating_id}",
    response_model=ModuleRatingRead,
    status_code=status.HTTP_200_OK,
)
def update_module_rating(
    rating_update: ModuleRatingUpdate,
    module_rating_id: int = Path(..., description="ID of the module rating to update"),
    year: str = Path(..., description="Academic year in short form e.g. 2324"),
    username: str = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    query = select(ModuleRating).where(ModuleRating.id == module_rating_id)
    module_rating = session.exec(query).first()
    if not module_rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module rating not found.",
        )

    if (
        module_rating.confidence_rating.username != username
        or module_rating.confidence_rating.year != year
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized"
        )

    if (rating_update.rating != -1) and (
        rating_update.rating < 1 or rating_update.rating > 5
    ):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Rating must be between 1 and 5.",
        )

    module_rating.rating = rating_update.rating
    session.commit()
    session.refresh(module_rating)
    return module_rating
