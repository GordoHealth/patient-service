import os
from unittest import mock

from fastapi import FastAPI, Depends, status
from fastapi.testclient import TestClient
import pytest
from pytest import LogCaptureFixture
from pytest_mock import MockerFixture

from app.logging import log_request_parameters, logging_policy
from app.middleware import LogRequestTimeMiddleware


app = FastAPI(dependencies=[Depends(log_request_parameters)])
app.add_middleware(LogRequestTimeMiddleware)


@app.get("/")
def get_a(param_1, param_2):
    return {"msg": "get A"}


@app.get("/{id}")
def get_a_detail(id):
    return {"msg": id}


@app.post("/")
def post_a(request_body: dict):
    return {"msg": request_body}


@app.put("/{id}")
def put_a(id, request_body: dict):
    return {"msg": id}


client = TestClient(app)


def test_logging_policy_only_unsecure_environments():
    with mock.patch.dict(os.environ, {"SECURE_BODY_LOGGING": "false"}):
        assert logging_policy() is False


def test_logging_policy_only_secure_environments():
    with mock.patch.dict(os.environ, {"SECURE_BODY_LOGGING": "true"}):
        assert logging_policy() is True


@pytest.fixture
def logging_policy_true(mocker):
    return mocker.patch("app.logging.logging_policy", return_value=True)


@pytest.fixture
def logging_policy_false(mocker):
    return mocker.patch("app.logging.logging_policy", return_value=False)


def test_logging_method_query_params(
    logging_policy_true: MockerFixture, caplog: LogCaptureFixture
):
    response = client.get("/", params={"param_1": "param_01", "param_2": "param_02"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"msg": "get A"}
    assert "(QUERY: param_1=param_01&param_2=param_02)" in caplog.text


def test_logging_method_path_params(
    logging_policy_true: MockerFixture, caplog: LogCaptureFixture
):
    random_id = "random-id"
    response = client.get(f"/{random_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"msg": random_id}
    assert "(PATH: {'id': 'random-id'})" in caplog.text


def test_logging_method_post_secure_env_set_true(
    logging_policy_true: MockerFixture, caplog: LogCaptureFixture
):
    response = client.post("/", json={"request_body": "content"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"msg": {"request_body": "content"}}
    assert "(BODY: Body parameters hidden due to secure logging policy)" in caplog.text


def test_logging_method_post_secure_env_set_false(
    logging_policy_false: MockerFixture, caplog: LogCaptureFixture
):
    response = client.post("/", json={"request_body": "content"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"msg": {"request_body": "content"}}
    assert "(BODY: {'request_body': 'content'})" in caplog.text


def test_logging_method_put_secure_env_set_true(
    logging_policy_true: MockerFixture, caplog: LogCaptureFixture
):
    response = client.put("/random-id", json={"request_body": "content"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"msg": "random-id"}
    assert "(BODY: Body parameters hidden due to secure logging policy)" in caplog.text


def test_logging_method_put_secure_env_set_false(
    logging_policy_false: MockerFixture, caplog: LogCaptureFixture
):
    response = client.put("/random-id", json={"request_body": "content"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"msg": "random-id"}
    assert "(BODY: {'request_body': 'content'})" in caplog.text
