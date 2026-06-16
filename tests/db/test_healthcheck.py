import pytest
from sqlalchemy import create_engine


from app.db.healthcheck import (
    check_database_connection, DBHealthStatus, DBStatus, DBHealthDetails)
from tests.config import test_db_config


pytestmark = pytest.mark.feature


def test_check_database_connection_healthy(mocker) -> None:
    engine = create_engine(test_db_config.database_url())

    mocker.patch("app.db.healthcheck.engine", engine)
    database_connection = check_database_connection()

    assert database_connection == DBHealthStatus(
        status=DBStatus.UP, details=DBHealthDetails(engine.name))


def test_check_database_connection_unhealthy(mocker) -> None:
    dummy_user = "username"
    dummy_passwd = 'password'
    engine = create_engine(
        f"postgresql://{dummy_user}:{dummy_passwd}@localhost:3306")

    mocker.patch("app.db.healthcheck.engine", engine)
    database_connection = check_database_connection()
    assert database_connection.status == DBStatus.DOWN
    assert database_connection.details.failure is not None


def test_check_database_connected_cannot_ping(mocker) -> None:
    mocker.patch("app.db.healthcheck.engine.connect") \
        .return_value.__enter__.return_value.execute \
        .return_value.scalar.return_value = 0
    database_connection = check_database_connection()

    assert database_connection.status == DBStatus.UNKNOWN
    assert database_connection.details.failure == "Can NOT ping to database"
