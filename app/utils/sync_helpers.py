import json
from fastapi import Depends
from datetime import datetime, timedelta, timezone
from sqlmodel import Session, select
from app.models.confidence_ratings import ConfidenceRating, ModuleRating
from app.models.user_sync_status import UserSyncStatus
from app.protocols import AbcUpstreamService

from app.dependencies.main import get_abc_service_handler, get_settings

SYNC_INTERVAL = timedelta(hours=24)


def get_sync_status(
    session: Session, year: str, username: str
) -> UserSyncStatus | None:
    query = select(UserSyncStatus).where(
        UserSyncStatus.year == year, UserSyncStatus.username == username
    )
    return session.exec(query).first()


def needs_sync(sync_status: UserSyncStatus | None) -> bool:
    if sync_status is None:
        return True
    return datetime.now(timezone.utc) - sync_status.last_synced > SYNC_INTERVAL


def update_sync_status(session: Session, year: str, username: str): 
    sync_status = get_sync_status(session, year, username)
    if sync_status:
        sync_status.last_synced = datetime.now(timezone.utc)
        session.add(sync_status)
    else:
        sync_status = UserSyncStatus(
            year=year, username=username, last_synced=datetime.now(timezone.utc)
        )
        session.add(sync_status)
    session.commit()


def create_missing_ratings(
    session: Session,
    year: str,
    username: str,
    total_weeks: int,
):
    query = select(ConfidenceRating).where(
        ConfidenceRating.year == year, ConfidenceRating.username == username
    )
    confidence_rating = session.exec(query).first()

    if not confidence_rating:
        confidence_rating = ConfidenceRating(year=year, username=username)
        session.add(confidence_rating)
        session.commit()
        session.refresh(confidence_rating)

    modules = get_module_list(year, username)
    if not modules:
        return

    existing_keys = {
        (mr.module_code, mr.term_week) for mr in confidence_rating.module_ratings
    }

    for module_code in modules:
        for week in range(1, total_weeks + 1):
            if (module_code, week) not in existing_keys:
                new_module_rating = ModuleRating(
                    module_code=module_code,
                    term_week=week,
                    rating=None,
                    confidence_rating_id=confidence_rating.id,
                )
                session.add(new_module_rating)

    session.commit()


def get_module_list(
    year: str,
    username: str,
) -> list[str]:
    settings = get_settings()
    abc_service = get_abc_service_handler(settings)
    response = abc_service.student_info(usernames=[username], year=year)
    data = json.loads(response.content)

    if not data:
        return []

    student = data[0]
    modules = student.get("modules", [])

    return [module["code"] for module in modules]
