import pytest
from uuid import uuid4

from app.db.exceptions import ResourceNotFoundException
from app.db.mappers.patient import PatientMapper
from app.db.models import Patient
from app.schemas.patient import PatientCreate, PatientSearch, PatientUpdate
from tests.conftest import reset_database, insert_to_db
from tests.factories.patient import PatientFactory

pytestmark = pytest.mark.feature


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    reset_database()
    yield
    reset_database()


def test_create_and_get_by_id():
    create_data = PatientFactory().create(PatientCreate)
    created = PatientMapper.create(create_data)
    fetched = PatientMapper.get_by_id(created.id)
    assert fetched.mrn == create_data.mrn


def test_search_by_last_name():
    patient = PatientFactory().create(Patient)
    insert_to_db(patient)
    results = PatientMapper.search(PatientSearch(last_name=patient.last_name))
    assert any(r.id == patient.id for r in results)


def test_update_sets_last_modified_by():
    create_data = PatientFactory().create(PatientCreate)
    created = PatientMapper.create(create_data)
    actor = uuid4()
    updated = PatientMapper.update(
        created.id,
        PatientUpdate(status=create_data.status, last_modified_by=actor),
    )
    assert updated.last_modified_by == actor


def test_delete_removes_record():
    create_data = PatientFactory().create(PatientCreate)
    created = PatientMapper.create(create_data)
    PatientMapper.delete(created.id)
    with pytest.raises(ResourceNotFoundException):
        PatientMapper.get_by_id(created.id)
