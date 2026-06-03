import psycopg2.errors
import pytest
from pytest_mock import MockerFixture
from sqlalchemy.exc import SQLAlchemyError, DBAPIError

from app.db import exceptions


def test_unexpected_sqlalchemy_error():
    error_message = "BOOM"

    with pytest.raises(Exception) as excinfo:
        with exceptions.db_error_manager():
            raise SQLAlchemyError(error_message)

    assert str(excinfo.value) == f"Unexpected DB Error: {error_message}"


def test_unexpected_db_api_error():
    error_message = "BOOM"

    with pytest.raises(Exception) as excinfo:
        with exceptions.db_error_manager():
            raise DBAPIError("", [], orig=Exception(error_message))

    assert str(excinfo.value) == (
        f"Unexpected DB Error: (builtins.Exception) {error_message}"
        "\n(Background on this error at: https://sqlalche.me/e/20/dbapi)"
    )


def test_unexpected_look_up_error():
    error_message = "BOOM"

    with pytest.raises(Exception) as excinfo:
        with exceptions.db_error_manager():
            raise LookupError(error_message)

    assert str(excinfo.value) == f"Error in looking for database: {error_message}"


def test_unique_violation_parser(mocker: MockerFixture):
    mock_error = mocker.MagicMock(spec=psycopg2.errors.UniqueViolation)
    mock_error.diag.table_name = "test_table"
    mock_error.diag.message_detail = "Key (test_field)=(test_value) already exists."

    with pytest.raises(Exception) as excinfo:
        with exceptions.db_error_manager():
            raise DBAPIError("", [], orig=mock_error)

    assert (
        str(excinfo.value)
        == "(test_table) already has a (test_field) with value (test_value)"
    )


def test_unique_violation_parser_with_empty_message_detail(mocker: MockerFixture):
    mock_error = mocker.MagicMock(spec=psycopg2.errors.UniqueViolation)
    mock_error.diag.table_name = "test_table"
    mock_error.diag.message_detail = ""

    with pytest.raises(Exception) as excinfo:
        with exceptions.db_error_manager():
            raise DBAPIError("", [], orig=mock_error)

    assert str(excinfo.value) == "Unexpected psycopg2 UniqueViolation message format: "


def test_unique_violation_parser_unknown_format(mocker: MockerFixture):
    mock_error = mocker.MagicMock(spec=psycopg2.errors.UniqueViolation)
    mock_error.diag.message_detail = "bad format"

    with pytest.raises(Exception) as excinfo:
        with exceptions.db_error_manager():
            raise DBAPIError("", [], orig=mock_error)

    assert (
        str(excinfo.value)
        == "Unexpected psycopg2 UniqueViolation message format: bad format"
    )
