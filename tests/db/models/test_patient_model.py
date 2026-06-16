import pytest

from app.db.exceptions import UniqueConstraintDBError
from app.db.models import Patient
from tests.conftest import reset_database, insert_to_db
from tests.factories.patient import PatientFactory

pytestmark = pytest.mark.feature


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    reset_database()
    yield
    reset_database()


def test_unique_mrn_constraint():
    patient = PatientFactory().create(Patient)
    insert_to_db(patient)
    duplicate = PatientFactory().create(Patient)
    duplicate.mrn = patient.mrn
    with pytest.raises(UniqueConstraintDBError):
        insert_to_db(duplicate)
