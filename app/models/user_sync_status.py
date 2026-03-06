from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional


class UserSyncStatus(SQLModel, table=True):
    __tablename__ = "user_sync_status"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    year: str = Field(index=True)
    last_synced: datetime = Field(default_factory=datetime.now(timezone.utc))
