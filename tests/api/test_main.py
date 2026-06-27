import pytest
import os
from unittest import mock
from pytest import LogCaptureFixture
from fastapi import status
from fastapi.testclient import TestClient

from app.config.environment import is_environment_remote
from app.main import app
from tests.conftest import OIDC_CLIENT_ID, OIDC_SERVER_URL


pytestmark = pytest.mark.feature

ENDPOINT = ""


def test_health_check(client: TestClient):
    response = client.get(f"{ENDPOINT}/health_check")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["healthy"] is True


def test_health_check_redirect_slash_be_disabled(client: TestClient):
    response = client.get(f"{ENDPOINT}/health_check/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_status(client: TestClient):
    response = client.get(f"{ENDPOINT}/status")
    assert response.status_code == status.HTTP_200_OK


def test_cors_policy_without_header_origin(client: TestClient):
    response = client.options(
        ENDPOINT, headers={"Access-Control-Request-Method": "GET"}
    )
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_cors_policy_without_header_request_method(client: TestClient):
    response = client.options(
        ENDPOINT, headers={"Origin": "https://api.2322.gordohealth.com"}
    )
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.parametrize(
    "allow_origin",
    [
        "http://localhost",
        "http://localhost:3000",
        "https://localhost",
        "https://localhost:4000",
    ],
)
@pytest.mark.skipif(is_environment_remote(), reason="only test with local domain")
def test_local_env_cors_policy_include_header_allow_origin(
    client: TestClient, allow_origin
):
    response = client.options(
        ENDPOINT,
        headers={"Origin": allow_origin, "Access-Control-Request-Method": "GET"},
    )
    assert response.status_code == status.HTTP_200_OK


def test_root_redirect(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.url.raw_path.decode("utf-8").endswith("/api/latest/docs")


def test_docs_redirect(client: TestClient):
    response = client.get("/docs")
    assert response.status_code == 200
    assert response.url.raw_path.decode("utf-8").endswith("/api/latest/docs")


def test_redoc_redirect(client: TestClient):
    response = client.get("/redoc")
    assert response.status_code == 200
    assert response.url.raw_path.decode("utf-8").endswith("/api/latest/redoc")


def test_initialize_oidc_failed(caplog: LogCaptureFixture):
    with mock.patch.dict(os.environ, {"OIDC_SERVER_URL": OIDC_SERVER_URL,
                                      "OIDC_CLIENT_ID": OIDC_CLIENT_ID}), TestClient(app):
        assert "Exception with oidc preparation" in caplog.text
