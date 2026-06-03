import pytest
from datetime import date
from uuid import uuid4
from fastapi import status
from fastapi.testclient import TestClient

from app.db.models import Patient, PatientStatus
from app.schemas.patient import PatientCreate
from tests.conftest import reset_database, insert_to_db
from tests.factories.patient import PatientFactory

ENDPOINT = "/api/v1/patients"

pytestmark = pytest.mark.feature


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    reset_database()
    yield
    reset_database()


@pytest.fixture(scope="module")
def patient_record():
    patient = PatientFactory().create(Patient)
    insert_to_db(patient)
    return patient


def test_get_patient_by_id(client: TestClient, patient_record: Patient):
    response = client.get(f"{ENDPOINT}/{patient_record.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == str(patient_record.id)
    assert data["mrn"] == patient_record.mrn


def test_get_patient_by_mrn(client: TestClient, patient_record: Patient):
    response = client.get(f"{ENDPOINT}/mrn/{patient_record.mrn}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["mrn"] == patient_record.mrn


def test_get_patient_not_found(client: TestClient):
    response = client.get(f"{ENDPOINT}/{uuid4()}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_search_patients_by_mrn(client: TestClient, patient_record: Patient):
    response = client.get(f"{ENDPOINT}", params={"mrn": patient_record.mrn})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1


def test_create_patient(client: TestClient):
    payload = PatientFactory().create(PatientCreate)
    response = client.post(f"{ENDPOINT}", json=payload.model_dump(mode="json"))
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["mrn"] == payload.mrn
    assert data["created_by"] == str(payload.created_by)


def test_update_patient(client: TestClient, patient_record: Patient):
    actor = uuid4()
    response = client.put(
        f"{ENDPOINT}/{patient_record.id}",
        json={
            "status": PatientStatus.discharged.value,
            "last_modified_by": str(actor),
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == PatientStatus.discharged.value
    assert response.json()["last_modified_by"] == str(actor)


def test_delete_patient(client: TestClient):
    patient = PatientFactory().create(Patient)
    insert_to_db(patient)
    response = client.delete(f"{ENDPOINT}/{patient.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert client.get(f"{ENDPOINT}/{patient.id}").status_code == status.HTTP_404_NOT_FOUND
