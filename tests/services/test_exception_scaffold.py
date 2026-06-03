import json
import uuid

from fastapi import Request, status
from sqlalchemy.exc import OperationalError
import pytest

from app.db.exceptions import DBError, DBLookupError, UnexpectedDBError, UniqueConstraintDBError
from app.services.exception_scaffold import ExceptionHandler


DATABASE_ERROR = "Database Error"


@pytest.fixture
def fastapi_request():
    request = Request({"type": "http"})
    request_uuid = str(uuid.uuid4())
    request.state.request_id = request_uuid
    return request


@pytest.fixture
def exception_handler() -> ExceptionHandler:
    handler = ExceptionHandler()
    return handler


def test_handler_manager_can_be_when_it_undefined(exception_handler: ExceptionHandler):
    assert exception_handler.log_handler_manager is not None


@pytest.mark.asyncio
async def test_db_error(
    exception_handler: ExceptionHandler,
    fastapi_request: Request,
    caplog: pytest.LogCaptureFixture
):
    exception_message = "Database Error"
    exception = DBError(exception_message)
    response = await exception_handler.db_error_handler(fastapi_request, exception)
    body = json.loads(response.body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert body["detail"] == exception_message
    last_log = caplog.records[-1]
    assert exception_message in last_log.message


@pytest.mark.asyncio
async def test_db_operational_error(
    exception_handler: ExceptionHandler,
    fastapi_request: Request,
    caplog: pytest.LogCaptureFixture
):
    exception_message = "Wrong password"
    exception = OperationalError(exception_message, {}, None)
    response = await exception_handler.db_error_handler(fastapi_request, exception)
    body = json.loads(response.body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert body["detail"] == DATABASE_ERROR
    last_log = caplog.records[-1]
    assert exception_message in last_log.message


@pytest.mark.asyncio
async def test_db_lookup_error(
    exception_handler: ExceptionHandler,
    fastapi_request: Request,
    caplog: pytest.LogCaptureFixture
):
    exception_message = "Look up error"
    exception = DBLookupError(exception_message)
    response = await exception_handler.db_error_handler(fastapi_request, exception)
    body = json.loads(response.body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert body["detail"] == DATABASE_ERROR
    last_log = caplog.records[-1]
    assert exception_message in last_log.message


@pytest.mark.asyncio
async def test_unique_constrain_dberror(
    exception_handler: ExceptionHandler,
    fastapi_request: Request,
    caplog: pytest.LogCaptureFixture
):
    exception_message = "Unique Constrain DB Error"
    exception = UniqueConstraintDBError(exception_message)
    response = await exception_handler.db_error_handler(fastapi_request, exception)
    body = json.loads(response.body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert body["detail"] == DATABASE_ERROR
    last_log = caplog.records[-1]
    assert exception_message in last_log.message


@pytest.mark.asyncio
async def test_unexpected_dberror(
    exception_handler: ExceptionHandler,
    fastapi_request: Request,
    caplog: pytest.LogCaptureFixture
):
    exception_message = "Unexpected Database Error"
    exception = UnexpectedDBError(exception_message)
    response = await exception_handler.db_error_handler(fastapi_request, exception)
    body = json.loads(response.body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert body["detail"] == DATABASE_ERROR
    last_log = caplog.records[-1]
    assert exception_message in last_log.message


@pytest.mark.asyncio
async def test_all_errors_handler_raises_exception(
    exception_handler: ExceptionHandler,
    fastapi_request: Request,
    caplog: pytest.LogCaptureFixture
):
    exception_message = "internal error"
    exception = Exception(exception_message)
    response = await exception_handler.all_errors_handler(fastapi_request, exception)
    body = json.loads(response.body)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert body["detail"] == "Internal Server Error"
    last_log = caplog.records[-1]
    assert exception_message in last_log.message
