import re
import pytest
from fastapi import status
from fastapi.testclient import TestClient

from tests.conftest import reset_database, DEVTOOLS_PASSWORD

pytestmark = pytest.mark.feature

ENDPOINT = "/devtools"


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    reset_database()
    yield
    reset_database()


def test_get_table_list(client: TestClient):
    response = client.get(
        f"{ENDPOINT}/db_tables",
        headers={"devtools-password": DEVTOOLS_PASSWORD},
    )
    assert response.status_code == status.HTTP_200_OK
    table_list = response.json()
    assert isinstance(table_list, list)
    expected = {
        "patients",
        "care_plans",
        "clinical_charts",
        "medications",
        "patient_medications",
    }
    for table in expected:
        assert table in table_list


def test_validation_with_wrong_devtools_password(client: TestClient):
    res = client.get(
        f"{ENDPOINT}/db_tables",
        headers={"devtools-password": f"wrong_{DEVTOOLS_PASSWORD}"},
    )
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
    assert re.search(r"Unable to authenticate request", str(res.json())) is not None
