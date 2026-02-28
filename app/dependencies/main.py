from functools import lru_cache
from typing import Generator

from fastapi import Depends, Header, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session
from starlette import status

from app.database.connection import engine
from app.dev_service_providers.ldap_authentication import DummyLdapAuthenticator
from app.dev_service_providers.abc_api_service import DummyAbcAPIService
from app.protocols import AbcUpstreamService, Authenticator
from app.settings import Settings

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Basic"},
)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as s:
        try:
            yield s
            s.commit()
        except SQLAlchemyError as e:
            s.rollback()
            raise e


@lru_cache()
def get_settings() -> Settings:
    return Settings()


def get_ldap_service(settings: Settings = Depends(get_settings)) -> Authenticator:
    if settings.is_production:
        raise RuntimeError("No production mode available yet.")
    return DummyLdapAuthenticator()


basic_auth = HTTPBasic(realm="DoC")


def get_current_user(
    credentials: HTTPBasicCredentials = Depends(basic_auth),
    ldap_handler: Authenticator = Depends(get_ldap_service),
    x_proxied_user: str = Header(default=None),
    settings: Settings = Depends(get_settings),
) -> str:
    username, password = (
        credentials.username.strip().lower(),
        credentials.password.strip(),
    )
    if ldap_handler.authenticate(username, password) is None:
        raise CREDENTIALS_EXCEPTION

    return (
        x_proxied_user
        if x_proxied_user and username in settings.super_users
        else username
    )


def get_abc_service_handler(
    settings: Settings = Depends(get_settings),
) -> AbcUpstreamService:
    if settings.environment == "production":
        raise RuntimeError("No production mode available yet.")
    return DummyAbcAPIService()
