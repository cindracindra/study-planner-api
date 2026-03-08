from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy import or_
from sqlmodel import Session, select
from starlette import status
from datetime import date

from app.dependencies.main import get_current_user, get_session
from app.clients.quotes_client import get_random_excuse, get_random_quote
from app.models.banner import Banner
from app.schemas.banner import BannerRead, BannerWrite

banner_router = APIRouter(
    prefix="/me/{year}/banner",
    tags=["banner"],
)


@banner_router.get("", response_model=BannerRead)
def get_daily_banner(
    year: str = Path(..., description="Academic year in short form e.g. 2324"),
    username: str = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    query = select(Banner).where(
        Banner.year == year,
        Banner.username == username,
    )
    result = session.exec(query).first()

    if not result:
        result = Banner(
            year=year,
            username=username,
            date=date.today(),
            banner_type="quote",
            display_text=get_random_quote(),
        )
        session.add(result)
        session.commit()
        session.refresh(result)
        return result

    # New day — refresh content
    if result.date != date.today():
        result.date = date.today()
        result.banner_type = "quote"
        result.display_text = get_random_quote()
        session.commit()

    return result


@banner_router.patch("", response_model=BannerRead)
def update_daily_banner(
    banner_update: BannerWrite,
    year: str = Path(..., description="Academic year in short form e.g. 2324"),
    username: str = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    query = select(Banner).where(
        Banner.year == year,
        Banner.username == username,
    )
    result = session.exec(query).first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Daily banner not found"
        )

    if banner_update.banner_type == "custom":
        if not banner_update.display_text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="display_text is required for custom banner.",
            )
        result.display_text = banner_update.display_text
    elif banner_update.banner_type == "excuse":
        result.display_text = get_random_excuse()
    else:
        result.display_text = get_random_quote()

    session.commit()
    return result
