import uuid
import os
import pytest
from unittest import mock
from fastapi.testclient import TestClient
from fastapi import Request
from pytest_mock import MockerFixture
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.orm.session import close_all_sessions
from app.db.models import Base
from app.db.session import get_db, db_session
from app.main import app, api_v1
from app.api.v1.app import verify_api_key
from tests.config import test_db_config


@pytest.fixture
def db(mocker: MockerFixture):
    db = mocker.MagicMock(name="db")
    return db


engine = None
TestSessionLocal = None


@pytest.fixture(scope="session", autouse=True)
def create_test_db(pytestconfig):
    # shortcircuit to not use database unless running feature tests
    if "not feature" == pytestconfig.getoption("-k"):
        return

    global engine
    global TestSessionLocal

    engine = create_engine(test_db_config.database_url())

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    TestSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    db_session.set(TestSessionLocal())


def reset_database():
    print("Reset database")
    close_all_sessions()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def insert_to_db(resource):
    db = db_session.get()
    try:
        db.add(resource)
        db.commit()
    except Exception as ex:
        db.rollback()
        raise ex


@pytest.fixture
def test_db():
    class TestingSession(Session):
        def commit(self):
            self.flush()
            self.expire_all()

    engine = create_engine(test_db_config.database_url())

    connection = engine.connect()
    trans = connection.begin()

    test_session_maker = sessionmaker(
        bind=engine, autoflush=False, autocommit=False, class_=TestingSession
    )
    test_session = test_session_maker()
    test_session.begin_nested()

    @event.listens_for(test_session, "after_transaction_end")
    def restart_savepoints(savepoint, transaction):
        if transaction.nested and not transaction._parent.nested:
            savepoint.expire_all()
            savepoint.begin_nested()

    yield test_session

    test_session.close()
    trans.rollback()
    connection.close()


OIDC_SERVER_URL = "https://example.org"
OIDC_CLIENT_ID = "license-testing-client"
DEVTOOLS_PASSWORD = "devtools-password"


@pytest.fixture
def client(test_db):
    def get_test_db():
        yield test_db

    app.dependency_overrides[get_db] = get_test_db
    api_v1.dependency_overrides[get_db] = get_test_db
    api_v1.dependency_overrides[verify_api_key] = lambda: None

    yield TestClient(app)


@pytest.fixture
def secure_client(test_db):
    def get_test_db():
        yield test_db

    app.dependency_overrides[get_db] = get_test_db
    api_v1.dependency_overrides[get_db] = get_test_db
    api_v1.dependency_overrides[verify_api_key] = verify_api_key

    yield TestClient(app)


@pytest.fixture
def get_request():
    scope = {
        "method": "GET",
        "path": "",
        "state": {},
        "type": "http",
        "headers": {},
        "query_string": "",
    }
    return Request(scope)


@pytest.fixture
def fastapi_request():
    request = Request({"type": "http"})
    request_uuid = str(uuid.uuid4())
    request.state.request_id = request_uuid
    return request
