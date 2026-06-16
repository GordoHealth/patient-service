import pytest
from uuid import uuid4
from fastapi import status
from fastapi.testclient import TestClient

from app.schemas.medication import MedicationCreate
from tests.factories.medication import MedicationFactory

ENDPOINT = "/api/v1/medications"

pytestmark = pytest.mark.feature


def test_create_and_get_medication(client: TestClient):
    payload = MedicationFactory().create(MedicationCreate)
    create_response = client.post(
        f"{ENDPOINT}", json=payload.model_dump(mode="json")
    )
    assert create_response.status_code == status.HTTP_201_CREATED
    medication_id = create_response.json()["id"]
    get_response = client.get(f"{ENDPOINT}/{medication_id}")
    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.json()["name"] == payload.name


def test_get_medication_not_found(client: TestClient):
    response = client.get(f"{ENDPOINT}/{uuid4()}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
