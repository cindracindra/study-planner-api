# ruff: noqa: E402
import os
from contextlib import contextmanager
from unittest import mock
from unittest.mock import Mock

import pytest
from alembic import command
from alembic.config import Config
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from pytest_factoryboy import register
from requests.auth import HTTPBasicAuth
from sqlalchemy_utils import create_database, database_exists, drop_database
from sqlmodel import Session, create_engine

from app.doc_upstream_services.abc.api_service import AbcAPIService
from app.doc_upstream_services.abc.deserialisation import S
from app.factories import orm_factories, abc_factories
from app.utils.factories import set_factories_session

TEST_DB_SERVER_URL: str = os.environ.get("TEST_DB_SERVER_URL", "postgresql://") # TODO: Set up test database 
HPOTTER_CREDENTIALS = HTTPBasicAuth(username="hpotter", password="leviosa")
ADUMBLE_CREDENTIALS = HTTPBasicAuth(username="adumble", password="password")


mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

from app import create_application
from app.dependencies.main import (
    basic_auth,
    get_abc_service_handler,
    get_current_user,
    get_session,
    get_settings,
)
from app.settings import Settings

for factory in orm_factories + abc_factories:
    register(factory)


@pytest.fixture(name="db_engine", scope="session")
def db_engine_fixture():
    engine = create_engine(f"{TEST_DB_SERVER_URL}/test-module_subscriptions")
    if database_exists(engine.url):
        # Catch case in which previous test run failed without teardown
        drop_database(engine.url)
    create_database(engine.url)
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", str(engine.url))
    command.upgrade(alembic_cfg, "head")
    yield engine
    drop_database(engine.url)


@pytest.fixture(name="session", autouse=True)
def session_fixture(db_engine):
    connection = db_engine.connect()

    transaction = connection.begin()
    with Session(connection) as session:
        set_factories_session(orm_factories, session)
        yield session
        transaction.rollback()
        connection.close()


@pytest.fixture(name="app")
def app_fixture(session: Session):
    app: FastAPI = create_application()

    def get_session_override():
        yield session

    def get_settings_override():
        return Settings(testing=True)

    def get_current_user_override(token=Depends(basic_auth)):
        return token.username

    def get_abc_service_handler_override():
        return Mock(AbcAPIService)

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[get_settings] = get_settings_override
    app.dependency_overrides[get_current_user] = get_current_user_override
    app.dependency_overrides[get_abc_service_handler] = get_abc_service_handler_override

    yield app
    app.dependency_overrides.clear()


@pytest.fixture(name="client")
def client_fixture(app) -> TestClient:
    return TestClient(app)


@pytest.fixture(name="abc_patched_client")
def abc_patched_client_fixture(app):
    """Fixture to create test client with patched ABC service.

    Returns a context manager function that configures ABC mocks for testing.

    Usage:
        abc_config = {
            "get_student": RestrictedStudentPersonalDetails(...),
        }

        with abc_patched_client(abc_config) as client:
            res = client.post("/endpoint", json=payload, auth=HPOTTER_CREDENTIALS)
    """

    @contextmanager
    def _abc_patched_client(conf: dict[str, type[S]]):
        def abc_override():
            mock_abc = Mock(AbcAPIService)
            for method, return_val in conf.items():
                setattr(mock_abc, method, Mock(return_value=return_val))
            return mock_abc

        app.dependency_overrides[get_abc_service_handler] = abc_override
        yield TestClient(app)

    return _abc_patched_client


@pytest.fixture(name="student_abc_config")
def student_abc_config(restricted_student_personal_details_factory):
    return {
        "get_student": restricted_student_personal_details_factory(
            login="hpotter",
            degree_year="mc3",
        )
    }
